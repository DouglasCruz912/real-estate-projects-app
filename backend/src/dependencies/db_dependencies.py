"""
Dependencias de base de datos para FastAPI
Simplificadas y fáciles de usar
"""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import redis.asyncio as redis

from ..database.connection import get_db_session, get_redis


# Dependencia principal para sesiones de BD
async def get_db() -> AsyncSession:
    """Obtener sesión de base de datos"""
    async for session in get_db_session():
        yield session


# Dependencia para Redis (opcional)
async def get_redis_client() -> Optional[redis.Redis]:
    """Obtener cliente Redis (puede ser None)"""
    return await get_redis()


# Alias para uso más limpio en routers
DatabaseDep = Depends(get_db)
RedisDep = Depends(get_redis_client) 