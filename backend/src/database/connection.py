"""
Conexión simple a la base de datos MySQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
import structlog
from typing import Optional, AsyncGenerator
import redis.asyncio as redis

from .config import db_config
from .base import Base

logger = structlog.get_logger()

# Variables globales
engine: Optional[create_async_engine] = None
session_maker: Optional[async_sessionmaker] = None
redis_client: Optional[redis.Redis] = None


async def init_db():
    """Inicializar conexión a la base de datos"""
    global engine, session_maker, redis_client
    
    try:
        # Crear engine MySQL
        engine = create_async_engine(
            db_config.database_url,
            echo=False,  # Deshabilitado para producción
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        # Crear session maker
        session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        # Inicializar Redis (opcional)
        try:
            redis_client = redis.from_url(db_config.redis_url, decode_responses=True)
            await redis_client.ping()
            logger.info("✅ Redis conectado", host=db_config.REDIS_HOST)
        except Exception as e:
            logger.warning("⚠️ Redis no disponible", error=str(e))
            redis_client = None
        
        # Verificar MySQL
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("✅ Base de datos conectada", 
                   host=db_config.HOST, 
                   database=db_config.NAME)
        
    except Exception as e:
        logger.error("❌ Error conectando base de datos", error=str(e))
        raise


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Obtener sesión de base de datos (dependencia FastAPI)"""
    if not session_maker:
        raise RuntimeError("Base de datos no inicializada")
    
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_redis() -> Optional[redis.Redis]:
    """Obtener cliente Redis (puede ser None si no está disponible)"""
    return redis_client


async def create_tables():
    """Crear todas las tablas"""
    if not engine:
        raise RuntimeError("Engine no inicializado")
    
    # IMPORTANTE: Importar modelos aquí para asegurar que estén en metadata
    try:
        from ..models import (
            RbacUser,
            RealEstateCompany,
            Project, 
            ProjectStock,
            ProjectImage,
            LegalUser,
            ProjectDocument
        )
        logger.info("📦 Modelos importados para creación de tablas")
    except ImportError as e:
        logger.error(f"❌ Error importando modelos: {e}")
        raise e
    
    # Verificar que tenemos tablas para crear
    tables = list(Base.metadata.tables.keys())
    logger.info(f"🔨 Creando {len(tables)} tablas: {tables}")
    
    if not tables:
        logger.warning("⚠️ No se encontraron modelos para crear tablas")
        return "⚠️ No se encontraron modelos para crear tablas"
    
    # Crear solo las tablas nuevas (rbac_users ya existe)
    async with engine.begin() as conn:
        def create_new_tables(connection):
            # Obtener todas las tablas definidas
            all_tables = Base.metadata.tables
            
            # Tablas que NO deben crearse (ya existen)
            existing_tables = {"rbac_users"}
            
            # Crear solo las tablas nuevas
            for table_name, table in all_tables.items():
                if table_name not in existing_tables:
                    table.create(connection, checkfirst=True)
        
        await conn.run_sync(create_new_tables)
    
    logger.info("✅ Tablas nuevas creadas correctamente")
    return "✅ Tablas nuevas creadas correctamente"


async def check_health() -> dict:
    """Verificar estado de la base de datos"""
    health = {"mysql": False, "redis": False}
    
    # MySQL
    try:
        if engine:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            health["mysql"] = True
    except Exception:
        pass
    
    # Redis
    try:
        if redis_client:
            await redis_client.ping()
            health["redis"] = True
    except Exception:
        pass
    
    return health


async def close_db():
    """Cerrar conexiones"""
    global engine, redis_client
    
    if engine:
        await engine.dispose()
    
    if redis_client:
        await redis_client.close()
    
    logger.info("🔒 Conexiones cerradas")


 