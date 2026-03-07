"""
Router para manejo de archivos (imágenes y documentos)
Integrado con AWS S3 bucket-api-projects
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
import structlog

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAPIKey
from ..services.s3_service import s3_service
from ..services.project_image_service import (
    create_project_images,
    get_project_images,
    get_project_images_summary,
    update_project_image,
    delete_project_image
)
from ..services.project_document_service import (
    create_project_document,
    get_project_documents,
    update_project_document,
    delete_project_document
)
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.base import BaseResponse

logger = structlog.get_logger()

router = APIRouter()


@router.post("/project/{project_id}/images", response_model=dict)
async def upload_project_images(
    project_id: int = Path(..., description="ID del proyecto"),
    files: List[UploadFile] = File(..., description="Archivos de imagen"),
    broker_email: str = Query(..., description="Email del broker que realiza la operación"),
    image_type: str = Query("general", description="Tipo de imagen"),
    alt_text: Optional[str] = Query(None, description="Texto alternativo"),
    is_featured: bool = Query(False, description="Marcar como imagen destacada"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Subir imágenes de proyecto a S3 y guardar en base de datos
    
    Todas las imágenes se guardan como un solo registro con URLs separadas por comas
    Las imágenes se organizan automáticamente en carpetas por nombre del proyecto
    
    - **project_id**: ID del proyecto
    - **files**: Lista de archivos de imagen
    - **broker_email**: Email del broker responsable
    - **image_type**: Tipo de imagen (general, exterior, interior, plano, etc.)
    - **alt_text**: Texto alternativo para accesibilidad
    - **is_featured**: Marcar como imagen destacada del proyecto
    """
    try:
        # Validar que hay archivos
        if not files or len(files) == 0:
            raise HTTPException(
                status_code=400,
                detail="Se requiere al menos un archivo de imagen"
            )
        
        # Validar límite de archivos
        if len(files) > 10:
            raise HTTPException(
                status_code=400,
                detail="No se pueden subir más de 10 imágenes a la vez"
            )
        
        # Validar que todos los archivos son imágenes
        for file in files:
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400,
                    detail=f"El archivo {file.filename} no es una imagen válida"
                )
            
            # Validar tamaño (max 10MB por imagen)
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"La imagen {file.filename} es muy grande (máx 10MB)"
                )
            await file.seek(0)  # Resetear el archivo
        
        # Subir imágenes y guardar en base de datos
        project_image = await create_project_images(
            db=db,
            project_id=project_id,
            files=files,
            broker_email=broker_email,
            image_type=image_type,
            alt_text=alt_text,
            is_featured=is_featured
        )
        
        # Separar URLs para respuesta
        urls_list = project_image.url.split(',') if project_image.url else []
        
        # Extraer información del bucket y keys desde las URLs
        bucket_name = "bucket-api-projects"
        keys_list = []
        for url in urls_list:
            if "bucket-api-projects.s3." in url:
                # Extraer la key desde la URL
                key = url.split("bucket-api-projects.s3.us-west-2.amazonaws.com/")[1]
                keys_list.append(key)
        
        return {
            "success": True,
            "message": f"Se subieron {len(files)} imágenes exitosamente",
            "data": {
                "project_image_id": project_image.id,
                "project_id": project_id,
                "filename": project_image.filename,
                "image_type": project_image.image_type,
                "is_featured": project_image.is_featured,
                "display_order": project_image.display_order,
                "total_images": len(files),
                "bucket": bucket_name,
                "keys_list": keys_list,
                "urls_list": urls_list,
                "created_at": project_image.created_at.isoformat() if project_image.created_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error subiendo imágenes de proyecto", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/project/{project_id}/images", response_model=dict)
async def get_project_images_list(
    project_id: int = Path(..., description="ID del proyecto"),
    image_type: Optional[str] = Query(None, description="Filtrar por tipo de imagen"),
    is_featured: Optional[bool] = Query(None, description="Filtrar por imagen destacada"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Obtener imágenes de un proyecto desde la base de datos
    
    - **project_id**: ID del proyecto
    - **image_type**: Filtrar por tipo específico de imagen
    - **is_featured**: Filtrar solo imágenes destacadas
    """
    try:
        # Obtener imágenes desde la base de datos
        images = await get_project_images(
            db=db,
            project_id=project_id,
            image_type=image_type,
            is_featured=is_featured
        )
        
        # Procesar imágenes para respuesta
        processed_images = []
        all_urls = []
        
        for image in images:
            urls = image.url.split(',') if image.url else []
            all_urls.extend(urls)
            
            processed_images.append({
                "id": image.id,
                "filename": image.filename,
                "image_type": image.image_type,
                "is_featured": image.is_featured,
                "is_active": image.is_active,
                "display_order": image.display_order,
                "alt_text": image.alt_text,
                "urls_list": urls,
                "individual_images_count": len(urls),
                "created_at": image.created_at.isoformat() if image.created_at else None
            })
        
        return {
            "success": True,
            "message": f"Imágenes del proyecto {project_id} desde base de datos",
            "data": {
                "project_id": project_id,
                "total_image_records": len(images),
                "total_individual_images": len(all_urls),
                "images": processed_images,
                "all_urls_list": all_urls
            }
        }
        
    except Exception as e:
        logger.error("Error obteniendo imágenes de proyecto", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/project/{project_id}/images/summary", response_model=dict)
async def get_project_images_summary_endpoint(
    project_id: int = Path(..., description="ID del proyecto"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Obtener resumen de imágenes del proyecto
    
    - **project_id**: ID del proyecto
    """
    try:
        summary = await get_project_images_summary(db=db, project_id=project_id)
        
        return {
            "success": True,
            "message": f"Resumen de imágenes del proyecto {project_id}",
            "data": summary
        }
        
    except Exception as e:
        logger.error("Error obteniendo resumen de imágenes", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/project-image/{image_id}", response_model=dict)
async def update_project_image_endpoint(
    image_id: int = Path(..., description="ID de la imagen"),
    broker_email: str = Query(..., description="Email del broker que realiza la operación"),
    image_type: Optional[str] = Query(None, description="Tipo de imagen"),
    alt_text: Optional[str] = Query(None, description="Texto alternativo"),
    is_featured: Optional[bool] = Query(None, description="Marcar como destacada"),
    is_active: Optional[bool] = Query(None, description="Activar/desactivar imagen"),
    display_order: Optional[int] = Query(None, description="Orden de visualización"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Actualizar información de imagen de proyecto
    
    - **image_id**: ID de la imagen
    - **broker_email**: Email del broker responsable
    """
    try:
        # Preparar datos de actualización
        update_data = {}
        if image_type is not None:
            update_data["image_type"] = image_type
        if alt_text is not None:
            update_data["alt_text"] = alt_text
        if is_featured is not None:
            update_data["is_featured"] = is_featured
        if is_active is not None:
            update_data["is_active"] = is_active
        if display_order is not None:
            update_data["display_order"] = display_order
        
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Se requiere al menos un campo para actualizar"
            )
        
        # Actualizar imagen
        image = await update_project_image(
            db=db,
            image_id=image_id,
            update_data=update_data,
            broker_email=broker_email
        )
        
        # Separar URLs para respuesta
        urls_list = image.url.split(',') if image.url else []
        
        return {
            "success": True,
            "message": "Imagen actualizada exitosamente",
            "data": {
                "id": image.id,
                "project_id": image.project_id,
                "filename": image.filename,
                "image_type": image.image_type,
                "is_featured": image.is_featured,
                "is_active": image.is_active,
                "display_order": image.display_order,
                "alt_text": image.alt_text,
                "urls_list": urls_list,
                "updated_at": image.updated_at.isoformat() if image.updated_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error actualizando imagen de proyecto", image_id=image_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/project-image/{image_id}", response_model=dict)
async def delete_project_image_endpoint(
    image_id: int = Path(..., description="ID de la imagen"),
    broker_email: str = Query(..., description="Email del broker que realiza la operación"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Eliminar imagen de proyecto (soft delete)
    
    - **image_id**: ID de la imagen
    - **broker_email**: Email del broker responsable
    """
    try:
        await delete_project_image(
            db=db,
            image_id=image_id,
            broker_email=broker_email
        )
        
        return {
            "success": True,
            "message": "Imagen eliminada exitosamente",
            "data": {
                "image_id": image_id,
                "deleted_at": "now"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error eliminando imagen de proyecto", image_id=image_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/project/{project_id}/documents", response_model=dict)
async def upload_project_document(
    project_id: int = Path(..., description="ID del proyecto"),
    file: UploadFile = File(..., description="Archivo de documento"),
    broker_email: str = Query(..., description="Email del broker que realiza la operación"),
    document_type: str = Query("general", description="Tipo de documento"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Subir documento de proyecto a S3 y guardar en base de datos
    
    El documento se organiza automáticamente en carpeta por nombre del proyecto
    
    - **project_id**: ID del proyecto
    - **file**: Archivo de documento (PDF, DOC, DOCX, etc.)
    - **broker_email**: Email del broker que realiza la operación
    - **document_type**: Tipo de documento (general, contrato, plano, etc.)
    """
    try:
        # Validar tipo de archivo
        allowed_types = [
            'application/pdf',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/plain'
        ]
        
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail="Tipo de archivo no permitido. Solo se permiten: PDF, DOC, DOCX, XLS, XLSX, TXT"
            )
        
        # Validar tamaño (max 25MB para documentos)
        content = await file.read()
        file_size = len(content)
        
        if file_size > 25 * 1024 * 1024:  # 25MB
            raise HTTPException(
                status_code=400,
                detail="El archivo no puede ser mayor a 25MB"
            )
        
        # Resetear el archivo
        await file.seek(0)
        
        # Subir documento y guardar en base de datos
        project_document = await create_project_document(
            db=db,
            project_id=project_id,
            file=file,
            broker_email=broker_email,
            document_type=document_type
        )
        
        return {
            "success": True,
            "message": "Documento subido exitosamente",
            "data": {
                "document_id": project_document.id,
                "project_id": project_id,
                "filename": project_document.filename,
                "url": project_document.url,
                "document_type": project_document.document_type,
                "is_active": project_document.is_active,
                "created_at": project_document.created_at.isoformat() if project_document.created_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error subiendo documento de proyecto", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.get("/project/{project_id}/documents", response_model=dict)
async def get_project_documents_list(
    project_id: int = Path(..., description="ID del proyecto"),
    document_type: Optional[str] = Query(None, description="Filtrar por tipo de documento"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Obtener documentos de un proyecto desde la base de datos
    
    - **project_id**: ID del proyecto
    - **document_type**: Filtrar por tipo específico de documento
    """
    try:
        # Obtener documentos desde la base de datos
        documents = await get_project_documents(
            db=db,
            project_id=project_id,
            document_type=document_type
        )
        
        # Procesar documentos para respuesta
        processed_documents = []
        
        for document in documents:
            processed_documents.append({
                "id": document.id,
                "filename": document.filename,
                "url": document.url,
                "document_type": document.document_type,
                "is_active": document.is_active,
                "created_at": document.created_at.isoformat() if document.created_at else None
            })
        
        return {
            "success": True,
            "message": f"Documentos del proyecto {project_id} desde base de datos",
            "data": {
                "project_id": project_id,
                "total_documents": len(documents),
                "documents": processed_documents
            }
        }
        
    except Exception as e:
        logger.error("Error obteniendo documentos de proyecto", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/project-document/{document_id}", response_model=dict)
async def update_project_document_endpoint(
    document_id: int = Path(..., description="ID del documento"),
    broker_email: str = Query(..., description="Email del broker que realiza la operación"),
    document_type: Optional[str] = Query(None, description="Tipo de documento"),
    is_active: Optional[bool] = Query(None, description="Activar/desactivar documento"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Actualizar información de documento de proyecto
    
    - **document_id**: ID del documento
    - **broker_email**: Email del broker responsable
    - **document_type**: Tipo de documento
    - **is_active**: Activar/desactivar documento
    """
    try:
        # Preparar datos de actualización
        update_data = {}
        if document_type is not None:
            update_data["document_type"] = document_type
        if is_active is not None:
            update_data["is_active"] = is_active
        
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="Se requiere al menos un campo para actualizar"
            )
        
        # Actualizar documento
        document = await update_project_document(
            db=db,
            document_id=document_id,
            update_data=update_data,
            broker_email=broker_email
        )
        
        return {
            "success": True,
            "message": "Documento actualizado exitosamente",
            "data": {
                "id": document.id,
                "project_id": document.project_id,
                "filename": document.filename,
                "url": document.url,
                "document_type": document.document_type,
                "is_active": document.is_active,
                "updated_at": document.updated_at.isoformat() if document.updated_at else None
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error actualizando documento de proyecto", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.delete("/project-document/{document_id}", response_model=dict)
async def delete_project_document_endpoint(
    document_id: int = Path(..., description="ID del documento"),
    broker_email: str = Query(..., description="Email del broker que realiza la operación"),
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    """
    Eliminar documento de proyecto (soft delete)
    
    - **document_id**: ID del documento
    - **broker_email**: Email del broker responsable
    """
    try:
        await delete_project_document(
            db=db,
            document_id=document_id,
            broker_email=broker_email
        )
        
        return {
            "success": True,
            "message": "Documento eliminado exitosamente",
            "data": {
                "document_id": document_id,
                "deleted_at": "now"
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error eliminando documento de proyecto", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")