"""
Módulo de routers FastAPI completo
"""

from fastapi import APIRouter
from . import companies, projects, stock, files

# Router principal que incluye todos los subrouters
main_router = APIRouter()

# Incluir todos los routers
main_router.include_router(companies.router, prefix="/api/companies", tags=["Inmobiliarias"])
main_router.include_router(projects.router, prefix="/api/projects", tags=["Proyectos"])
main_router.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
main_router.include_router(files.router, prefix="/api/files", tags=["Archivos"])

__all__ = ["main_router"] 