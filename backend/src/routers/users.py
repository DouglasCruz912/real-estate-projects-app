"""
Router CRUD de usuarios (requiere rol admin)
"""

from typing import List
from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAdmin
from ..services import user_service
from ..utils.exceptions import APIException
from ..schemas.users import UserCreate, UserUpdate, UserResponse
from ..models import User

router = APIRouter()


@router.get("", response_model=List[UserResponse])
async def list_users(
    db: AsyncSession = DatabaseDep,
    _admin: User = RequireAdmin,
):
    """Listar todos los usuarios"""
    users = await user_service.list_users(db)
    return [UserResponse.model_validate(u) for u in users]


@router.post("", response_model=UserResponse, status_code=201)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = DatabaseDep,
    _admin: User = RequireAdmin,
):
    """Crear un nuevo usuario"""
    try:
        user = await user_service.create_user(db, user_data.model_dump())
        return UserResponse.model_validate(user)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = DatabaseDep,
    _admin: User = RequireAdmin,
):
    """Obtener usuario por ID"""
    user = await user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return UserResponse.model_validate(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    update_data: UserUpdate,
    db: AsyncSession = DatabaseDep,
    _admin: User = RequireAdmin,
):
    """Actualizar usuario"""
    try:
        user = await user_service.update_user(db, user_id, update_data.model_dump(exclude_unset=True))
        return UserResponse.model_validate(user)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{user_id}", status_code=200)
async def delete_user(
    user_id: int,
    db: AsyncSession = DatabaseDep,
    _admin: User = RequireAdmin,
):
    """Desactivar usuario (soft delete)"""
    try:
        return await user_service.delete_user(db, user_id)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
