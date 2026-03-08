"""
Conexión a la base de datos MySQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
import structlog
from typing import Optional, AsyncGenerator

from .config import db_config
from .base import Base

logger = structlog.get_logger()

engine: Optional[create_async_engine] = None
session_maker: Optional[async_sessionmaker] = None


async def init_db():
    """Inicializar conexión a la base de datos"""
    global engine, session_maker
    
    try:
        engine = create_async_engine(
            db_config.database_url,
            echo=False,
            pool_pre_ping=True,
            pool_recycle=3600
        )
        
        session_maker = async_sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False
        )
        
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("Base de datos conectada", 
                   host=db_config.HOST, 
                   database=db_config.NAME)
        
    except Exception as e:
        logger.error("Error conectando base de datos", error=str(e))
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


async def create_tables():
    """Crear todas las tablas"""
    if not engine:
        raise RuntimeError("Engine no inicializado")
    
    try:
        from ..models import (
            User,
            RealEstateCompany,
            Project, 
            ProjectStock,
            ProjectImage,
            LegalUser,
            ProjectDocument,
            ProjectCommercial
        )
        logger.info("Modelos importados para creación de tablas")
    except ImportError as e:
        logger.error(f"Error importando modelos: {e}")
        raise e
    
    tables = list(Base.metadata.tables.keys())
    logger.info(f"Creando {len(tables)} tablas: {tables}")
    
    if not tables:
        logger.warning("No se encontraron modelos para crear tablas")
        return "No se encontraron modelos para crear tablas"
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Tablas creadas correctamente")
    return "Tablas creadas correctamente"


async def check_health() -> dict:
    """Verificar estado de la base de datos"""
    health = {"mysql": False}
    
    try:
        if engine:
            async with engine.begin() as conn:
                await conn.execute(text("SELECT 1"))
            health["mysql"] = True
    except Exception:
        pass
    
    return health


async def close_db():
    """Cerrar conexiones"""
    global engine
    
    if engine:
        await engine.dispose()
    
    logger.info("Conexiones cerradas")
