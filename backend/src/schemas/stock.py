"""
Schemas de Pydantic para Stock de Proyectos
Modelos de request/response para el CRUD de stock
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal
from datetime import date, datetime
from .base import BaseResponse
from ..utils.constants import UNIT_TYPES, STOCK_STATES, CURRENCY_TYPES, ORIENTATION_TYPES



class StockCreateRequest(BaseModel):
    """Schema para crear unidad de stock"""
    project_id: int = Field(..., gt=0, description="ID del proyecto")
    unit_number: str = Field(..., min_length=1, max_length=50, description="Número de unidad")
    unit_type: str = Field(..., max_length=50, description="Tipo de unidad")
    description: Optional[str] = Field(None, description="Descripción de la unidad")
    
    # Características básicas
    bedrooms: int = Field(0, ge=0, le=20, description="Número de dormitorios")
    bathrooms: int = Field(0, ge=0, le=20, description="Número de baños")
    orientation: Optional[str] = Field(None, max_length=50, description="Orientación de la unidad")
    total_area: Optional[Decimal] = Field(None, gt=0, description="Área total en m²")
    
    # Ubicación
    floor: Optional[int] = Field(None, description="Piso")
    building: Optional[str] = Field(None, max_length=50, description="Edificio/Torre")
    
    # Estacionamientos y bodegas
    parkings: Optional[str] = Field(None, max_length=50, description="Información de estacionamientos")
    storages: Optional[str] = Field(None, max_length=50, description="Información de bodegas")
    has_parking: bool = Field(False, description="Tiene estacionamiento")
    has_storage: bool = Field(False, description="Tiene bodega")
    
    # Superficies (todas en m²)
    surface_internal: Optional[Decimal] = Field(None, ge=0, description="Superficie interna en m²")
    surface_terrace: Optional[Decimal] = Field(None, ge=0, description="Superficie terraza en m²")
    surface_garden: Optional[Decimal] = Field(None, ge=0, description="Superficie jardín en m²")
    surface_pantry: Optional[Decimal] = Field(None, ge=0, description="Superficie despensa en m²")
    surface_multiuse_assignable: Optional[Decimal] = Field(None, ge=0, description="Superficie multiuso asignable en m²")
    surface_util: Optional[Decimal] = Field(None, ge=0, description="Superficie útil en m²")
    surface_terrain: Optional[Decimal] = Field(None, ge=0, description="Superficie terreno en m²")
    surface_others: Optional[Decimal] = Field(None, ge=0, description="Otras superficies en m²")
    
    # Precios y valores
    currency: str = Field(default="CLP", max_length=10, description="Moneda")
    value_base: Optional[Decimal] = Field(None, ge=0, description="Precio base")
    value_uf: Optional[Decimal] = Field(None, ge=0, description="Precio en UF")
    value_list: Optional[Decimal] = Field(None, ge=0, description="Precio de lista")
    value_discount: Optional[Decimal] = Field(None, ge=0, description="Descuento aplicado")
    value_enabled: Optional[Decimal] = Field(None, ge=0, description="Valor habilitado")
    value_promotion: Optional[Decimal] = Field(None, ge=0, description="Valor promocional")
    value_bonus: Optional[Decimal] = Field(None, ge=0, description="Bono aplicado")
    value_parking: Optional[Decimal] = Field(None, ge=0, description="Valor del estacionamiento")
    value_storage: Optional[Decimal] = Field(None, ge=0, description="Valor de la bodega")
    
    # Estado
    status: str = Field(default="available", description="Estado de la unidad")
    
    @validator('unit_type')
    def validate_unit_type(cls, v):
        if v not in UNIT_TYPES.values():
            raise ValueError(f'unit_type must be one of: {", ".join(UNIT_TYPES.values())}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in STOCK_STATES:
            raise ValueError(f'status must be one of: {", ".join(STOCK_STATES)}')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        if v not in CURRENCY_TYPES:
            raise ValueError(f'currency must be one of: {", ".join(CURRENCY_TYPES)}')
        return v
    
    @validator('orientation')
    def validate_orientation(cls, v):
        if v is not None:
            if v.lower() not in ORIENTATION_TYPES:
                raise ValueError(f'orientation must be one of: {", ".join(ORIENTATION_TYPES)}')
        return v


class StockUpdateRequest(BaseModel):
    """Schema para actualizar unidad de stock"""
    unit_number: Optional[str] = Field(None, min_length=1, max_length=50, description="Número de unidad")
    unit_type: Optional[str] = Field(None, max_length=50, description="Tipo de unidad")
    description: Optional[str] = Field(None, description="Descripción de la unidad")
    
    # Características básicas
    bedrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de dormitorios")
    bathrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de baños")
    orientation: Optional[str] = Field(None, max_length=50, description="Orientación de la unidad")
    total_area: Optional[Decimal] = Field(None, gt=0, description="Área total en m²")
    
    # Ubicación
    floor: Optional[int] = Field(None, description="Piso")
    building: Optional[str] = Field(None, max_length=50, description="Edificio/Torre")
    
    # Estacionamientos y bodegas
    parkings: Optional[str] = Field(None, max_length=50, description="Información de estacionamientos")
    storages: Optional[str] = Field(None, max_length=50, description="Información de bodegas")
    has_parking: Optional[bool] = Field(None, description="Tiene estacionamiento")
    has_storage: Optional[bool] = Field(None, description="Tiene bodega")
    
    # Superficies (todas en m²)
    surface_internal: Optional[Decimal] = Field(None, ge=0, description="Superficie interna en m²")
    surface_terrace: Optional[Decimal] = Field(None, ge=0, description="Superficie terraza en m²")
    surface_garden: Optional[Decimal] = Field(None, ge=0, description="Superficie jardín en m²")
    surface_pantry: Optional[Decimal] = Field(None, ge=0, description="Superficie despensa en m²")
    surface_multiuse_assignable: Optional[Decimal] = Field(None, ge=0, description="Superficie multiuso asignable en m²")
    surface_util: Optional[Decimal] = Field(None, ge=0, description="Superficie útil en m²")
    surface_terrain: Optional[Decimal] = Field(None, ge=0, description="Superficie terreno en m²")
    surface_others: Optional[Decimal] = Field(None, ge=0, description="Otras superficies en m²")
    
    # Precios y valores
    currency: Optional[str] = Field(None, max_length=10, description="Moneda")
    value_base: Optional[Decimal] = Field(None, ge=0, description="Precio base")
    value_uf: Optional[Decimal] = Field(None, ge=0, description="Precio en UF")
    value_list: Optional[Decimal] = Field(None, ge=0, description="Precio de lista")
    value_discount: Optional[Decimal] = Field(None, ge=0, description="Descuento aplicado")
    value_enabled: Optional[Decimal] = Field(None, ge=0, description="Valor habilitado")
    value_promotion: Optional[Decimal] = Field(None, ge=0, description="Valor promocional")
    value_bonus: Optional[Decimal] = Field(None, ge=0, description="Bono aplicado")
    value_parking: Optional[Decimal] = Field(None, ge=0, description="Valor del estacionamiento")
    value_storage: Optional[Decimal] = Field(None, ge=0, description="Valor de la bodega")
    
    # Estado
    status: Optional[str] = Field(None, description="Estado de la unidad")


    @validator('unit_type')
    def validate_unit_type(cls, v):
        if v not in UNIT_TYPES.values():
            raise ValueError(f'unit_type must be one of: {", ".join(UNIT_TYPES.values())}')
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in STOCK_STATES:
            raise ValueError(f'status must be one of: {", ".join(STOCK_STATES)}')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        if v not in CURRENCY_TYPES:
            raise ValueError(f'currency must be one of: {", ".join(CURRENCY_TYPES)}')
        return v
    
    @validator('orientation')
    def validate_orientation(cls, v):
        if v is not None:
            if v.lower() not in ORIENTATION_TYPES:
                raise ValueError(f'orientation must be one of: {", ".join(ORIENTATION_TYPES)}')
        return v


class StockResponse(BaseResponse):
    """Schema de respuesta para unidad de stock"""
    id: int
    project_id: int
    unit_number: str
    unit_type: str
    description: Optional[str]
    
    # Características básicas
    bedrooms: int
    bathrooms: int
    orientation: Optional[str]
    total_area: Optional[Decimal]
    
    # Ubicación
    floor: Optional[int]
    building: Optional[str]
    
    # Estacionamientos y bodegas
    parkings: Optional[str]
    storages: Optional[str]
    has_parking: bool
    has_storage: bool
    
    # Superficies (todas en m²)
    surface_internal: Optional[Decimal]
    surface_terrace: Optional[Decimal]
    surface_garden: Optional[Decimal]
    surface_pantry: Optional[Decimal]
    surface_multiuse_assignable: Optional[Decimal]
    surface_util: Optional[Decimal]
    surface_terrain: Optional[Decimal]
    surface_others: Optional[Decimal]
    
    # Precios y valores
    currency: str
    value_base: Optional[Decimal]
    value_uf: Optional[Decimal]
    value_list: Optional[Decimal]
    value_discount: Optional[Decimal]
    value_enabled: Optional[Decimal]
    value_promotion: Optional[Decimal]
    value_bonus: Optional[Decimal]
    value_parking: Optional[Decimal]
    value_storage: Optional[Decimal]
    
    # Estado
    status: str
    
    # Metadatos
    created_at: datetime
    updated_at: datetime


class StockListResponse(BaseModel):
    """Schema para lista paginada de stock"""
    stock: List[StockResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class StockFilters(BaseModel):
    """Schema para filtros de búsqueda de stock"""
    project_id: Optional[int] = Field(None, ge=1, description="ID del proyecto")
    unit_type: Optional[str] = Field(None, description="Tipo de unidad")
    status: Optional[str] = Field(None, description="Estado de la unidad")
    
    # Características básicas
    bedrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de dormitorios")
    bathrooms: Optional[int] = Field(None, ge=0, le=20, description="Número de baños")
    orientation: Optional[str] = Field(None, description="Orientación de la unidad")
    
    # Ubicación
    building: Optional[str] = Field(None, description="Edificio/Torre")
    floor_min: Optional[int] = Field(None, description="Piso mínimo")
    floor_max: Optional[int] = Field(None, description="Piso máximo")
    
    # Precios
    currency: Optional[str] = Field(None, description="Moneda")
    price_min: Optional[Decimal] = Field(None, ge=0, description="Precio mínimo")
    price_max: Optional[Decimal] = Field(None, ge=0, description="Precio máximo")
    price_list_min: Optional[Decimal] = Field(None, ge=0, description="Precio de lista mínimo")
    price_list_max: Optional[Decimal] = Field(None, ge=0, description="Precio de lista máximo")
    parking_value_min: Optional[Decimal] = Field(None, ge=0, description="Valor mínimo de estacionamiento")
    parking_value_max: Optional[Decimal] = Field(None, ge=0, description="Valor máximo de estacionamiento")
    storage_value_min: Optional[Decimal] = Field(None, ge=0, description="Valor mínimo de bodega")
    storage_value_max: Optional[Decimal] = Field(None, ge=0, description="Valor máximo de bodega")
    
    # Áreas
    area_min: Optional[Decimal] = Field(None, gt=0, description="Área total mínima")
    area_max: Optional[Decimal] = Field(None, gt=0, description="Área total máxima")
    surface_internal_min: Optional[Decimal] = Field(None, ge=0, description="Superficie interna mínima")
    surface_internal_max: Optional[Decimal] = Field(None, ge=0, description="Superficie interna máxima")
    surface_util_min: Optional[Decimal] = Field(None, ge=0, description="Superficie útil mínima")
    surface_util_max: Optional[Decimal] = Field(None, ge=0, description="Superficie útil máxima")
    
    # Características booleanas
    available_only: bool = Field(False, description="Solo unidades disponibles")
    has_parking: Optional[bool] = Field(None, description="Tiene estacionamiento")
    has_storage: Optional[bool] = Field(None, description="Tiene bodega")


class StockStateUpdate(BaseModel):
    """Schema para actualización de estado del stock"""
    status: str = Field(..., description="Nuevo estado de la unidad")


class StockStats(BaseModel):
    """Schema para estadísticas de stock"""
    total_units: int = Field(..., description="Total de unidades")
    available_units: int = Field(..., description="Unidades disponibles")
    reserved_units: int = Field(..., description="Unidades reservadas")
    sold_units: int = Field(..., description="Unidades vendidas")
    avg_price: Optional[Decimal] = Field(None, description="Precio promedio")
    avg_area: Optional[Decimal] = Field(None, description="Área promedio") 