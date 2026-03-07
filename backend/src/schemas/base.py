"""
Schemas base de Pydantic
Contiene clases reutilizables para respuestas comunes
"""

from typing import List, Any, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime

# Type variable for generic pagination
T = TypeVar('T')


class BaseResponse(BaseModel):
    """Schema base para respuestas"""
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class MessageResponse(BaseModel):
    """Respuesta simple con mensaje"""
    message: str = Field(..., description="Mensaje de respuesta")
    success: bool = Field(True, description="Indica si la operación fue exitosa")
    data: Optional[Any] = Field(None, description="Datos adicionales opcionales")


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada genérica"""
    items: List[T] = Field(..., description="Lista de elementos")
    total: int = Field(..., ge=0, description="Total de elementos")
    page: int = Field(..., ge=1, description="Página actual")
    per_page: int = Field(..., ge=1, description="Elementos por página")
    total_pages: int = Field(..., ge=0, description="Total de páginas")
    
    @property
    def has_next(self) -> bool:
        """Verificar si hay página siguiente"""
        return self.page < self.total_pages
    
    @property
    def has_prev(self) -> bool:
        """Verificar si hay página anterior"""
        return self.page > 1


class ErrorResponse(BaseModel):
    """Schema para respuestas de error"""
    error: str = Field(..., description="Código de error")
    message: str = Field(..., description="Mensaje de error")
    detail: Optional[str] = Field(None, description="Detalles adicionales del error")
    path: Optional[str] = Field(None, description="Ruta donde ocurrió el error")
    timestamp: datetime = Field(default_factory=datetime.now, description="Momento del error")


class HealthResponse(BaseModel):
    """Schema para respuesta de health check"""
    status: str = Field(..., description="Estado general del servicio")
    version: str = Field(..., description="Versión de la API")
    timestamp: datetime = Field(default_factory=datetime.now, description="Momento de la verificación")
    services: Optional[dict] = Field(None, description="Estado de servicios dependientes")


class IdResponse(BaseModel):
    """Respuesta simple con ID"""
    id: int = Field(..., description="ID del elemento creado/afectado")
    message: Optional[str] = Field(None, description="Mensaje adicional") 