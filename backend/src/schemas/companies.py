"""
Schemas de Pydantic para Inmobiliarias
Modelos de request/response para el CRUD de companies
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, validator
from .base import BaseResponse
from ..utils.validation import validate_email, validate_tax_id

class CompanyCreate(BaseModel):
    """Schema para crear inmobiliaria"""
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la inmobiliaria")
    legal_name: Optional[str] = Field(None, max_length=255, description="Razón social")
    tax_id: Optional[str] = Field(None, max_length=20, description="Identificador fiscal (RUT, NIF, EIN, etc.)")
    email: Optional[str] = Field(None, max_length=255, description="Email principal")
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono principal")
    website: Optional[str] = Field(None, max_length=255, description="Sitio web")
    address: Optional[str] = Field(None, description="Dirección completa")
    city: Optional[str] = Field(None, max_length=100, description="Ciudad")
    region: Optional[str] = Field(None, max_length=100, description="Región / Estado / Provincia")
    is_active: bool = Field(True, description="Inmobiliaria activa")
    is_verified: bool = Field(False, description="Inmobiliaria verificada")
    
    @validator('email')
    def validate_email(cls, v):
        if v:
            valid, message = validate_email(v)
            if not valid:
                raise ValueError(message)
        return v
    
    @validator('tax_id')
    def validate_tax_id_field(cls, v):
        if v is not None and v:
            valid, message = validate_tax_id(v)
            if not valid:
                raise ValueError(message)
        return v


class CompanyUpdate(BaseModel):
    """Schema para actualizar inmobiliaria"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    legal_name: Optional[str] = Field(None, max_length=255)
    tax_id: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = None
    city: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=100)
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    
    @validator('email')
    def validate_email(cls, v):
        if v:
            valid, message = validate_email(v)
            if not valid:
                raise ValueError(message)
        return v


class CompanyResponse(BaseResponse):
    """Schema de respuesta para inmobiliaria"""
    id: int
    name: str
    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    address: Optional[str]
    city: Optional[str]
    region: Optional[str]
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


class CompanyStats(BaseModel):
    """Schema para estadísticas de inmobiliaria"""
    total_projects: int = Field(..., description="Total de proyectos")
    active_projects: int = Field(..., description="Proyectos activos")
    total_units: int = Field(..., description="Total de unidades")
    available_units: int = Field(..., description="Unidades disponibles")
    total_sales: int = Field(..., description="Total de ventas")
    
    
class CompanyListResponse(BaseModel):
    """Schema para lista paginada de inmobiliarias"""
    companies: list[CompanyResponse]
    total: int
    page: int
    per_page: int
    total_pages: int
