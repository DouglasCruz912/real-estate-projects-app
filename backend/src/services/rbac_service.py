"""
Servicio para operaciones RBAC
Manejo de usuarios y permisos
"""

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models import RbacUser
from ..utils.exceptions import APIException


async def get_user_id_by_email(db: AsyncSession, broker_email: str) -> int:
    """
    Obtener ID de usuario RBAC por email (nuser)
    
    Args:
        db: Sesión de base de datos
        broker_email: Email del broker (nuser)
        
    Returns:
        int: ID del usuario
        
    Raises:
        APIException: Si el usuario no existe o no está activo
    """
    
    if not broker_email:
        raise APIException(
            status_code=400,
            detail="Email del broker es requerido"
        )
    
    # Buscar usuario por nuser (email)
    query = select(RbacUser).where(
        RbacUser.nuser == broker_email
    )
    
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise APIException(
            status_code=404,
            detail=f"Usuario no encontrado con email: {broker_email}"
        )
    
    # Verificar que el usuario tenga staff válido
    if user.staff == 0:
        raise APIException(
            status_code=403,
            detail="Usuario no tiene permisos para crear proyectos"
        )
    
    return user.id


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[RbacUser]:
    """
    Obtener usuario RBAC por ID
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        
    Returns:
        RbacUser: Usuario encontrado o None
    """
    
    query = select(RbacUser).where(RbacUser.id == user_id)
    result = await db.execute(query)
    
    return result.scalar_one_or_none()


async def validate_user_permissions(db: AsyncSession, user_id: int, required_staff_level: int = 1) -> bool:
    """
    Validar permisos de usuario
    
    Args:
        db: Sesión de base de datos
        user_id: ID del usuario
        required_staff_level: Nivel de staff requerido
        
    Returns:
        bool: True si tiene permisos
    """
    
    user = await get_user_by_id(db, user_id)
    
    if not user:
        return False
    
    if user.staff < required_staff_level:
        return False
    
    if user.estado and user.estado.lower() != "activo":
        return False
    
    return True 