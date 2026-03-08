"""
Módulo de routers FastAPI completo
"""

from fastapi import APIRouter
from . import auth, users, companies, projects, stock, files

main_router = APIRouter()

main_router.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])
main_router.include_router(users.router, prefix="/api/users", tags=["Usuarios"])
main_router.include_router(companies.router, prefix="/api/companies", tags=["Inmobiliarias"])
main_router.include_router(projects.router, prefix="/api/projects", tags=["Proyectos"])
main_router.include_router(stock.router, prefix="/api/stock", tags=["Stock"])
main_router.include_router(files.router, prefix="/api/files", tags=["Archivos"])

__all__ = ["main_router"] 