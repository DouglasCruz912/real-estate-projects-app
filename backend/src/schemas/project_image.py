"""
Esquemas Pydantic para imágenes de proyectos
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ProjectImageBase(BaseModel):
    """Esquema base para imágenes de proyecto"""
    
    image_type: str = Field(..., description="Tipo de imagen")
    alt_text: Optional[str] = Field(None, description="Texto alternativo")
    is_featured: bool = Field(False, description="Imagen destacada")
    is_active: bool = Field(True, description="Imagen activa")
    display_order: int = Field(0, description="Orden de visualización")


class ProjectImageCreate(ProjectImageBase):
    """Esquema para crear imágenes de proyecto"""
    
    project_id: int = Field(..., description="ID del proyecto")
    
    @validator("image_type")
    def validate_image_type(cls, v):
        allowed_types = ["general", "exterior", "interior", "plano", "logo", "banner", "gallery"]
        if v not in allowed_types:
            raise ValueError(f"Tipo de imagen debe ser uno de: {allowed_types}")
        return v


class ProjectImageUpdate(BaseModel):
    """Esquema para actualizar imágenes de proyecto"""
    
    image_type: Optional[str] = Field(None, description="Tipo de imagen")
    alt_text: Optional[str] = Field(None, description="Texto alternativo")
    is_featured: Optional[bool] = Field(None, description="Imagen destacada")
    is_active: Optional[bool] = Field(None, description="Imagen activa")
    display_order: Optional[int] = Field(None, description="Orden de visualización")


class ProjectImageResponse(ProjectImageBase):
    """Esquema de respuesta para imágenes de proyecto"""
    
    id: int = Field(..., description="ID de la imagen")
    project_id: int = Field(..., description="ID del proyecto")
    filename: str = Field(..., description="Nombre del archivo")
    url: str = Field(..., description="URL de la imagen (puede contener múltiples URLs separadas por comas)")
    urls_list: List[str] = Field(default_factory=list, description="Lista de URLs individuales")
    individual_images_count: int = Field(0, description="Número de imágenes individuales")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de actualización")
    
    class Config:
        from_attributes = True
        
    @validator("urls_list", pre=True, always=True)
    def split_urls(cls, v, values):
        """Dividir URLs separadas por comas en una lista"""
        if "url" in values and values["url"]:
            return values["url"].split(",")
        return []
    
    @validator("individual_images_count", pre=True, always=True)
    def count_images(cls, v, values):
        """Contar número de imágenes individuales"""
        if "urls_list" in values:
            return len(values["urls_list"])
        return 0


class ProjectImageListResponse(BaseModel):
    """Esquema de respuesta para lista de imágenes de proyecto"""
    
    success: bool = Field(True, description="Éxito de la operación")
    message: str = Field(..., description="Mensaje de respuesta")
    data: dict = Field(..., description="Datos de respuesta")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Imágenes del proyecto 123 desde base de datos",
                "data": {
                    "project_id": 123,
                    "total_image_records": 3,
                    "total_individual_images": 8,
                    "images": [
                        {
                            "id": 1,
                            "filename": "3_images_batch.jpg",
                            "image_type": "general",
                            "is_featured": False,
                            "is_active": True,
                            "display_order": 1,
                            "alt_text": "Imágenes generales",
                            "urls_list": ["https://bucket.s3.amazonaws.com/1.jpg", "https://bucket.s3.amazonaws.com/2.jpg"],
                            "individual_images_count": 2
                        }
                    ],
                    "all_urls_list": ["https://bucket.s3.amazonaws.com/1.jpg", "https://bucket.s3.amazonaws.com/2.jpg"]
                }
            }
        }


class ProjectImageUploadResponse(BaseModel):
    """Esquema de respuesta para subida de imágenes"""
    
    success: bool = Field(True, description="Éxito de la operación")
    message: str = Field(..., description="Mensaje de respuesta")
    data: dict = Field(..., description="Datos de la imagen subida")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Se subieron 3 imágenes exitosamente",
                "data": {
                    "project_image_id": 1,
                    "project_id": 123,
                    "filename": "3_images_batch.jpg",
                    "image_type": "general",
                    "is_featured": False,
                    "display_order": 1,
                    "total_images": 3,
                    "bucket": "bucket-api-projects",
                    "keys_list": ["images/altos del cerro/image1.jpg", "images/altos del cerro/image2.jpg", "images/altos del cerro/image3.jpg"],
                    "urls_list": ["https://bucket-api-projects.s3.us-west-2.amazonaws.com/images/altos del cerro/image1.jpg", "https://bucket-api-projects.s3.us-west-2.amazonaws.com/images/altos del cerro/image2.jpg", "https://bucket-api-projects.s3.us-west-2.amazonaws.com/images/altos del cerro/image3.jpg"],
                    "created_at": "2025-01-07T10:00:00Z"
                }
            }
        }


class ProjectImageSummaryResponse(BaseModel):
    """Esquema de respuesta para resumen de imágenes"""
    
    success: bool = Field(True, description="Éxito de la operación")
    message: str = Field(..., description="Mensaje de respuesta")
    data: dict = Field(..., description="Resumen de imágenes")
    
    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Resumen de imágenes del proyecto 123",
                "data": {
                    "project_id": 123,
                    "total_image_records": 3,
                    "total_individual_images": 8,
                    "featured_image": 1,
                    "image_types": ["general", "exterior", "interior"],
                    "all_urls": ["https://bucket.s3.amazonaws.com/1.jpg", "https://bucket.s3.amazonaws.com/2.jpg"]
                }
            }
        } 