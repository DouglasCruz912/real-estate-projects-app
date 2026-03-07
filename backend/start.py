#!/usr/bin/env python3
"""
Script de inicio rápido para la API de Proyectos
Configura y ejecuta la API en modo desarrollo
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

import uvicorn
from src.database.connection import init_db, create_tables, check_health
from src.database.config import db_config
import structlog

logger = structlog.get_logger()


async def setup_database():
    """Configurar base de datos si es necesario"""
    try:
        logger.info("🔍 Verificando conexión a la base de datos...")
        await init_db()
        
        # Verificar salud de la BD
        health = await check_health()
        
        if health["mysql"]:
            logger.info("✅ Conexión MySQL establecida")
            
            # Crear tablas si no existen
            logger.info("🔨 Iniciando proceso de creación de tablas...")
            result = await create_tables()
            logger.info(f"✅ {result}")
        else:
            logger.error("❌ Error en MySQL")
            return False
        
        if health["redis"]:
            logger.info("✅ Conexión Redis establecida")
        else:
            logger.warning("⚠️ Redis no disponible")
        
        return True
        
    except Exception as e:
        logger.error("❌ Error configurando base de datos", error=str(e))
        return False


def main():
    """Función principal"""
    
    print("""
    🏢 API Proyectos Inmobiliarios v1.4.1
    ======================================
    
    Iniciando servidor de desarrollo...
    """)
    
    # Verificar configuración básica
    if not db_config.PASSWORD:
        logger.warning("⚠️ DB_PASSWORD no configurada, usando configuración por defecto")
    
    # Configurar uvicorn
    config = uvicorn.Config(
        "main:app",
        host="localhost",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
        reload_dirs=["."],
        reload_includes=["*.py"]
    )
    
    # Información de inicio
    print(f"""
    📍 Configuración:
    ├── Host: localhost:8000
    ├── Base de datos: {db_config.HOST}:{db_config.PORT}/{db_config.NAME}
    ├── Redis: {db_config.REDIS_HOST}:{db_config.REDIS_PORT}
    └── Log level: info
    
    🚀 Endpoints disponibles:
    ├── Documentación: http://localhost:8000/docs
    ├── ReDoc: http://localhost:8000/redoc
    ├── Health: http://localhost:8000/health
    ├── Root: http://localhost:8000/
    │
    ├── 🏢 Inmobiliarias:
    │   ├── GET    /api/companies
    │   ├── POST   /api/companies
    │   ├── GET    /api/companies/{{id}}
    │   ├── PUT    /api/companies/{{id}}
    │   └── DELETE /api/companies/{{id}}
    │
    ├── 🏗️ Proyectos:
    │   ├── GET    /api/projects
    │   ├── POST   /api/projects
    │   ├── GET    /api/projects/{{id}}
    │   ├── PUT    /api/projects/{{id}}
    │   └── DELETE /api/projects/{{id}}
    │
    ├── 📦 Stock:
    │   ├── GET    /api/stock
    │   ├── POST   /api/stock
    │   ├── GET    /api/stock/{{id}}
    │   ├── PUT    /api/stock/{{id}}
    │   └── DELETE /api/stock/{{id}}
    │
    └── 📁 Archivos:
        ├── Imágenes:
        │   ├── POST   /api/files/project/{{project_id}}/images
        │   ├── GET    /api/files/project/{{project_id}}/images
        │   ├── GET    /api/files/project/{{project_id}}/images/summary
        │   ├── PUT    /api/files/project-image/{{image_id}}
        │   └── DELETE /api/files/project-image/{{image_id}}
        │
        └── Documentos:
            ├── POST   /api/files/project/{{project_id}}/documents
            ├── GET    /api/files/project/{{project_id}}/documents
            ├── PUT    /api/files/project-document/{{document_id}}
            └── DELETE /api/files/project-document/{{document_id}}
    
    🔑 API Key: {db_config.API_KEY}
    
    💡 Nota: Todos los endpoints (excepto /health y /) requieren header 'X-API-Key'
    
    Presiona Ctrl+C para detener el servidor
    """)
    
    # Verificar base de datos antes de iniciar
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        db_ok = loop.run_until_complete(setup_database())
        
        if not db_ok:
            logger.error("❌ No se pudo conectar a la base de datos")
            sys.exit(1)
        
        logger.info("🚀 Iniciando servidor FastAPI...")
        
        # Iniciar servidor
        server = uvicorn.Server(config)
        loop.run_until_complete(server.serve())
        
    except KeyboardInterrupt:
        logger.info("🛑 Servidor detenido por el usuario")
    except Exception as e:
        logger.error("❌ Error inesperado", error=str(e))
        sys.exit(1)


if __name__ == "__main__":
    main() 