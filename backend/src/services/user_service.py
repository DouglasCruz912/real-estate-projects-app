"""
Servicio de negocio para Usuarios
"""

from typing import Optional, Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from ..models import User
from ..utils.exceptions import APIException, NotFoundError, ConflictError
from .auth_service import hash_password, verify_password


async def get_user_id_by_email(db: AsyncSession, email: str) -> int:
    """Obtener ID de usuario por email"""
    if not email:
        raise APIException(status_code=400, detail="Email del usuario es requerido")
    
    query = select(User).where(
        and_(User.email == email, User.is_active == True)
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError(f"Usuario no encontrado con email: {email}")
    return user.id


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Obtener usuario por ID"""
    query = select(User).where(
        and_(User.id == user_id, User.is_active == True)
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


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """Autenticar usuario por email y password. Retorna el User o None."""
    query = select(User).where(User.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


async def list_users(db: AsyncSession) -> List[User]:
    """Listar todos los usuarios"""
    query = select(User).order_by(User.id)
    result = await db.execute(query)
    return list(result.scalars().all())


async def create_user(db: AsyncSession, user_data: Dict[str, Any]) -> User:
    """Crear usuario con password hasheado"""
    await _validate_unique_email(db, user_data.get("email"))
    
    password = user_data.pop("password")
    user = User(**user_data, password_hash=hash_password(password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user(db: AsyncSession, user_id: int, update_data: Dict[str, Any]) -> User:
    """Actualizar usuario"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError(f"Usuario con ID {user_id} no encontrado")
    
    if "email" in update_data and update_data["email"] != user.email:
        await _validate_unique_email(db, update_data["email"])
    
    if "password" in update_data:
        user.password_hash = hash_password(update_data.pop("password"))
    
    for key, value in update_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    await db.commit()
    await db.refresh(user)
    return user


async def delete_user(db: AsyncSession, user_id: int) -> Dict[str, Any]:
    """Desactivar usuario (soft delete via is_active)"""
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise NotFoundError(f"Usuario con ID {user_id} no encontrado")
    
    user.is_active = False
    await db.commit()
    return {"message": f"Usuario {user.email} desactivado", "id": user_id}


async def _validate_unique_email(db: AsyncSession, email: Optional[str]) -> None:
    """Verificar que el email no esté en uso"""
    if not email:
        return
    query = select(func.count(User.id)).where(User.email == email)
    result = await db.execute(query)
    count = result.scalar()
    if count and count > 0:
        raise ConflictError(f"El email '{email}' ya está registrado")
