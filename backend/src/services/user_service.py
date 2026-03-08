"""
Servicio de negocio para Usuarios
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from ..models import User
from ..utils.exceptions import APIException, NotFoundError


async def get_user_id_by_email(db: AsyncSession, email: str) -> int:
    """Obtener ID de usuario por email"""
    
    if not email:
        raise APIException(
            status_code=400,
            detail="Email del usuario es requerido"
        )
    
    query = select(User).where(
        and_(
            User.email == email,
            User.is_active == True
        )
    )
    
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError(f"Usuario no encontrado con email: {email}")
    
    return user.id


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Obtener usuario por ID"""
    
    query = select(User).where(
        and_(
            User.id == user_id,
            User.is_active == True
        )
    )
    result = await db.execute(query)
    
    return result.scalar_one_or_none()


async def validate_user_permissions(db: AsyncSession, user_id: int, required_role: str = "user") -> bool:
    """Validar permisos de usuario por rol"""
    
    user = await get_user_by_id(db, user_id)
    
    if not user:
        return False
    
    role_hierarchy = {"admin": 3, "editor": 2, "user": 1}
    user_level = role_hierarchy.get(user.role, 0)
    required_level = role_hierarchy.get(required_role, 0)
    
    return user_level >= required_level
