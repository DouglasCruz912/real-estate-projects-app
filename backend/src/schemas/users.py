"""
Esquemas Pydantic para Users
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class UserBase(BaseModel):
    """Esquema base para usuario"""
    full_name: str = Field(..., min_length=1, max_length=255, description="Nombre completo del usuario")
    email: str = Field(..., max_length=255, description="Email del usuario")
    phone: Optional[str] = Field(None, max_length=50, description="Número de teléfono")
    role: str = Field(default="user", description="Rol del usuario")


class UserCreate(UserBase):
    """Esquema para crear usuario"""
    password: str = Field(..., min_length=8, description="Contraseña del usuario")


class UserUpdate(BaseModel):
    """Esquema para actualizar usuario"""
    full_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Nombre completo")
    email: Optional[str] = Field(None, max_length=255, description="Email")
    phone: Optional[str] = Field(None, max_length=50, description="Teléfono")
    role: Optional[str] = Field(None, description="Rol del usuario")
    is_active: Optional[bool] = Field(None, description="Estado activo")


class UserResponse(UserBase):
    """Esquema de respuesta para usuario"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(description="ID único del usuario")
    is_active: bool = Field(description="Estado activo del usuario")
    created_at: datetime = Field(description="Fecha de creación")
    updated_at: datetime = Field(description="Fecha de última actualización")


class UserInfo(BaseModel):
    """Información básica del usuario para auditoría"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(description="ID del usuario")
    full_name: str = Field(description="Nombre completo")
    email: str = Field(description="Email del usuario")


class LoginRequest(BaseModel):
    """Esquema para login"""
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña")


class LoginResponse(BaseModel):
    """Respuesta de login"""
    token: str = Field(description="JWT token")
    user: UserResponse = Field(description="Datos del usuario")
