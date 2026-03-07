"""
Esquemas Pydantic para RBAC
Validación de usuarios y permisos
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class RbacUserBase(BaseModel):
    """Esquema base para usuario RBAC"""
    nomcompleto: Optional[str] = Field(None, description="Nombre completo del usuario")
    nuser: Optional[str] = Field(None, description="Email/nombre de usuario único")
    telefono: Optional[str] = Field(None, description="Número de teléfono")
    staff: int = Field(description="Nivel de staff del usuario")
    estado: Optional[str] = Field(None, description="Estado del usuario")


class RbacUserResponse(RbacUserBase):
    """Esquema de respuesta para usuario RBAC"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(description="ID único del usuario")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    update_at: datetime = Field(description="Fecha de última actualización")


class RbacUserInfo(BaseModel):
    """Información básica del usuario para auditoría"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(description="ID del usuario")
    nomcompleto: Optional[str] = Field(None, description="Nombre completo")
    nuser: Optional[str] = Field(None, description="Email/usuario") 