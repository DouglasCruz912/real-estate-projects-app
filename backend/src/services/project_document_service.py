"""
Servicio para gestión de documentos de proyectos
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func, desc
from fastapi import UploadFile
import structlog

from ..models import ProjectDocument, Project
from ..utils.exceptions import (
    APIException,
    ProjectNotFoundError,
    ValidationError,
    DatabaseError
)
from . import user_service
from .s3_service import s3_service

logger = structlog.get_logger()


async def create_project_document(
    db: AsyncSession,
    project_id: int,
    file: UploadFile,
    broker_email: str,
    document_type: str = "general"
) -> ProjectDocument:
    """
    Crear registro de documento de proyecto
    Sube el archivo a S3 y guarda la información en la base de datos
    """
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Validar que el proyecto existe y obtener su información
        project = await _get_project_by_id(db, project_id)
        
        # Usar el nombre del proyecto como carpeta
        project_folder = project.name
        
        # Subir archivo a S3 usando el nombre del proyecto como carpeta
        result = await s3_service.upload_file(
            file=file,
            file_type="document",
            project_id=None,  # No usar project_id automático
            folder=project_folder  # Usar solo el nombre del proyecto
        )
        
        # Crear registro en la base de datos
        project_document = ProjectDocument(
            project_id=project_id,
            filename=result["filename"],
            url=result["url"],
            document_type=document_type,
            is_active=True,
            created_by=user_id
        )
        
        db.add(project_document)
        await db.commit()
        await db.refresh(project_document)
        
        logger.info(
            "Documento de proyecto creado",
            document_id=project_document.id,
            project_id=project_id,
            project_name=project.name,
            filename=result["filename"],
            document_type=document_type,
            created_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return project_document
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error creando documento de proyecto", error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_project_documents(
    db: AsyncSession,
    project_id: int,
    document_type: Optional[str] = None,
    is_active: bool = True
) -> List[ProjectDocument]:
    """Obtener documentos de un proyecto"""
    
    try:
        query = select(ProjectDocument).where(
            and_(
                ProjectDocument.project_id == project_id,
                ProjectDocument.deleted_at.is_(None)
            )
        )
        
        if document_type:
            query = query.where(ProjectDocument.document_type == document_type)
        
        if is_active is not None:
            query = query.where(ProjectDocument.is_active == is_active)
        
        query = query.order_by(desc(ProjectDocument.created_at))
        
        result = await db.execute(query)
        documents = result.scalars().all()
        
        return list(documents)
        
    except Exception as e:
        logger.error("Error obteniendo documentos de proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def update_project_document(
    db: AsyncSession,
    document_id: int,
    update_data: Dict[str, Any],
    broker_email: str
) -> ProjectDocument:
    """Actualizar documento de proyecto"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Obtener documento
        document = await get_project_document_by_id(db, document_id)
        
        # Actualizar campos
        for field, value in update_data.items():
            if hasattr(document, field):
                setattr(document, field, value)
        
        document.updated_by = user_id
        
        await db.commit()
        await db.refresh(document)
        
        logger.info(
            "Documento de proyecto actualizado",
            document_id=document.id,
            updated_fields=list(update_data.keys()),
            updated_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return document
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, APIException):
            raise e
        logger.error("Error actualizando documento", document_id=document_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def delete_project_document(
    db: AsyncSession,
    document_id: int,
    broker_email: str
) -> bool:
    """Eliminar documento de proyecto (soft delete)"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Obtener documento
        document = await get_project_document_by_id(db, document_id)
        
        # Soft delete
        document.deleted_at = func.now()
        document.deleted_by = user_id
        document.updated_by = user_id
        document.is_active = False
        
        await db.commit()
        
        logger.info(
            "Documento de proyecto eliminado",
            document_id=document.id,
            deleted_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return True
        
    except Exception as e:
        await db.rollback()
        if isinstance(e, APIException):
            raise e
        logger.error("Error eliminando documento", document_id=document_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_project_document_by_id(
    db: AsyncSession,
    document_id: int
) -> ProjectDocument:
    """Obtener documento por ID"""
    
    try:
        query = select(ProjectDocument).where(
            and_(
                ProjectDocument.id == document_id,
                ProjectDocument.deleted_at.is_(None)
            )
        )
        
        result = await db.execute(query)
        document = result.scalar_one_or_none()
        
        if not document:
            raise ValidationError(f"Documento con ID {document_id} no encontrado")
        
        return document
        
    except ValidationError:
        raise
    except Exception as e:
        logger.error("Error obteniendo documento por ID", document_id=document_id, error=str(e))
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