"""
Servicio para gestión de imágenes de proyectos
Guarda múltiples imágenes como un solo registro con URLs separadas por comas
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from fastapi import UploadFile
import structlog

from ..models import ProjectImage, Project
from ..utils.exceptions import (
    APIException,
    ProjectNotFoundError,
    ValidationError,
    DatabaseError
)
from . import user_service
from .s3_service import s3_service

logger = structlog.get_logger()


async def create_project_images(
    db: AsyncSession,
    project_id: int,
    files: List[UploadFile],
    broker_email: str,
    image_type: str = "general",
    alt_text: Optional[str] = None,
    is_featured: bool = False
) -> ProjectImage:
    """
    Crear registro de imágenes de proyecto
    Sube múltiples archivos a S3 y guarda las URLs en un solo registro
    Las imágenes se organizan automáticamente en carpetas por nombre del proyecto
    """
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Validar que el proyecto existe y obtener su información
        project = await _get_project_by_id(db, project_id)
        
        # Usar el nombre del proyecto como carpeta
        project_folder = project.name
        
        # Subir todas las imágenes a S3
        uploaded_files = []
        uploaded_urls = []
        
        for file in files:
            # Subir archivo a S3 usando el nombre del proyecto como carpeta
            # Pasar project_id=None para evitar que se agregue automáticamente project_{id}
            result = await s3_service.upload_file(
                file=file,
                file_type="image",
                project_id=None,  # No usar project_id automático
                folder=project_folder  # Usar solo el nombre del proyecto
            )
            
            uploaded_files.append(result)
            uploaded_urls.append(result["url"])
        
        # Crear string con URLs separadas por comas
        urls_comma_separated = ",".join(uploaded_urls)
        
        # Obtener el siguiente display_order
        display_order = await _get_next_display_order(db, project_id)
        
        # Crear registro único con todas las URLs
        project_image = ProjectImage(
            project_id=project_id,
            filename=uploaded_files[0]['original_filename'] if len(files) == 1 else f"{len(files)} imágenes",
            url=urls_comma_separated,  # URLs separadas por comas
            alt_text=alt_text,
            image_type=image_type,
            is_featured=is_featured,
            is_active=True,
            display_order=display_order,
            created_by=user_id
        )
        
        db.add(project_image)
        await db.commit()
        await db.refresh(project_image)
        
        logger.info(
            "Imágenes de proyecto creadas",
            project_image_id=project_image.id,
            project_id=project_id,
            project_name=project.name,
            images_count=len(files),
            created_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return project_image
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error creando imágenes de proyecto", error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_project_images(
    db: AsyncSession,
    project_id: int,
    image_type: Optional[str] = None,
    is_featured: Optional[bool] = None,
    is_active: bool = True
) -> List[ProjectImage]:
    """Obtener imágenes de un proyecto"""
    
    try:
        query = select(ProjectImage).where(
            and_(
                ProjectImage.project_id == project_id,
                ProjectImage.deleted_at.is_(None)
            )
        )
        
        if image_type:
            query = query.where(ProjectImage.image_type == image_type)
        
        if is_featured is not None:
            query = query.where(ProjectImage.is_featured == is_featured)
        
        if is_active is not None:
            query = query.where(ProjectImage.is_active == is_active)
        
        query = query.order_by(desc(ProjectImage.is_featured), ProjectImage.display_order)
        
        result = await db.execute(query)
        images = result.scalars().all()
        
        return list(images)
        
    except Exception as e:
        logger.error("Error obteniendo imágenes de proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def update_project_image(
    db: AsyncSession,
    image_id: int,
    update_data: Dict[str, Any],
    broker_email: str
) -> ProjectImage:
    """Actualizar imagen de proyecto"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Obtener imagen
        image = await get_project_image_by_id(db, image_id)
        
        # Actualizar campos
        for field, value in update_data.items():
            if hasattr(image, field):
                setattr(image, field, value)
        
        image.updated_by = user_id
        
        await db.commit()
        await db.refresh(image)
        
        logger.info(
            "Imagen de proyecto actualizada",
            image_id=image.id,
            updated_fields=list(update_data.keys()),
            updated_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return image
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, APIException):
            raise e
        logger.error("Error actualizando imagen", image_id=image_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def delete_project_image(
    db: AsyncSession,
    image_id: int,
    broker_email: str
) -> bool:
    """Eliminar imagen de proyecto (soft delete)"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Obtener imagen
        image = await get_project_image_by_id(db, image_id)
        
        # Soft delete
        image.deleted_at = func.now()
        image.deleted_by = user_id
        image.updated_by = user_id
        
        await db.commit()
        
        logger.info(
            "Imagen de proyecto eliminada",
            image_id=image.id,
            deleted_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return True
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, APIException):
            raise e
        logger.error("Error eliminando imagen", image_id=image_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_project_image_by_id(
    db: AsyncSession,
    image_id: int
) -> ProjectImage:
    """Obtener imagen por ID"""
    
    try:
        query = select(ProjectImage).where(
            and_(
                ProjectImage.id == image_id,
                ProjectImage.deleted_at.is_(None)
            )
        )
        
        result = await db.execute(query)
        image = result.scalar_one_or_none()
        
        if not image:
            raise ValidationError(f"Imagen con ID {image_id} no encontrada")
        
        return image
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error("Error obteniendo imagen por ID", image_id=image_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")





async def get_project_images_summary(
    db: AsyncSession,
    project_id: int
) -> Dict[str, Any]:
    """Obtener resumen de imágenes del proyecto"""
    
    try:
        images = await get_project_images(db, project_id)
        
        # Separar URLs y contar
        all_urls = []
        for image in images:
            urls = image.url.split(',') if image.url else []
            all_urls.extend(urls)
        
        # Buscar imagen destacada
        featured_image = None
        for image in images:
            if image.is_featured:
                featured_image = image
                break
        
        summary = {
            "project_id": project_id,
            "total_image_records": len(images),
            "total_individual_images": len(all_urls),
            "featured_image": featured_image.id if featured_image else None,
            "image_types": list(set(img.image_type for img in images)),
            "all_urls": all_urls
        }
        
        return summary
        
    except Exception as e:
        logger.error("Error obteniendo resumen de imágenes", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


# Funciones auxiliares privadas
async def _get_project_by_id(db: AsyncSession, project_id: int) -> Project:
    """Obtener proyecto por ID y validar que existe"""
    
    query = select(Project).where(
        and_(
            Project.id == project_id,
            Project.deleted_at.is_(None)
        )
    )
    
    project = await db.scalar(query)
    if not project:
        raise ProjectNotFoundError(project_id)
    
    return project


async def _get_next_display_order(db: AsyncSession, project_id: int) -> int:
    """Obtener el siguiente display_order para el proyecto"""
    
    query = select(func.max(ProjectImage.display_order)).where(
        and_(
            ProjectImage.project_id == project_id,
            ProjectImage.deleted_at.is_(None)
        )
    )
    
    result = await db.scalar(query)
    return (result or 0) + 1


 