"""
Router de autenticación: login y datos del usuario actual
"""

from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAuth
from ..services import user_service
from ..services.auth_service import create_access_token
from ..schemas.users import LoginRequest, LoginResponse, UserResponse
from ..models import User

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(data: LoginRequest, db: AsyncSession = DatabaseDep):
    """Autenticar usuario y obtener JWT token"""
    user = await user_service.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return LoginResponse(token=token, user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = RequireAuth):
    """Obtener datos del usuario autenticado"""
    return UserResponse.model_validate(current_user)
