"""
API de Proyectos Inmobiliarios
FastAPI con configuración simplificada
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
import structlog

# Imports internos
from src.database.connection import init_db, close_db, check_health
from src.routers import main_router
from src.middleware.auth import SimpleLoggingMiddleware

# Import mangum
from mangum import Mangum

logger = structlog.get_logger()

# Configuración de seguridad para Swagger UI
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión de ciclo de vida de la aplicación"""
    # Startup
    logger.info("🚀 Iniciando API de Proyectos...")
    await init_db()
    logger.info("✅ Base de datos conectada")
    
    yield
    
    # Shutdown  
    logger.info("🛑 Cerrando API de Proyectos...")
    await close_db()
    logger.info("✅ Conexiones cerradas")


# Crear aplicación FastAPI
app = FastAPI(
    title="API Proyectos Inmobiliarios", 
    description="API REST para gestión de proyectos y stock inmobiliario",
    version="1.4.1",
    lifespan=lifespan,
    # Configuración de seguridad para documentación
    openapi_tags=[
        {
            "name": "Inmobiliarias",
            "description": "Gestión de empresas inmobiliarias - **Requiere API Key**"
        },
        {
            "name": "Proyectos", 
            "description": "Gestión de proyectos inmobiliarios - **Requiere API Key**"
        },
        {
            "name": "Stock",
            "description": "Gestión de unidades de stock - **Requiere API Key**"
        },
        {
            "name": "Archivos",
            "description": "Gestión de imágenes y documentos - **Requiere API Key**"
        }
    ]
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SimpleLoggingMiddleware)

# Rutas
app.include_router(main_router)


# Endpoint de salud simple (público)
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificar estado de la aplicación"""
    health_status = await check_health()
    
    return {
        "status": "healthy" if health_status["mysql"] else "unhealthy",
        "database": health_status["mysql"],
        "version": "1.4.1"
    }


# Endpoint raíz (público)
@app.get("/", tags=["Sistema"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API Proyectos Inmobiliarios",
        "version": "1.4.1",
        "docs": "/docs",
        "health": "/health",
        "authentication": "Requiere header 'X-API-Key' para endpoints protegidos"
    }


# Crear instancia de Mangum
handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000) 