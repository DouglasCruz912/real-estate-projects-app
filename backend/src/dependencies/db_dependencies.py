"""
Dependencias de base de datos para FastAPI
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection import get_db_session


async def get_db() -> AsyncSession:
    """Obtener sesión de base de datos"""
    async for session in get_db_session():
        yield session


DatabaseDep = Depends(get_db)
