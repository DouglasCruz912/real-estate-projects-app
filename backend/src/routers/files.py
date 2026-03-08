"""
Router para manejo de archivos (imágenes y documentos)
Integrado con AWS S3 / MinIO (bucket configurado via AWS_S3_BUCKET_NAME)
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from typing import List, Optional
import structlog

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAuth
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
from ..models import User

logger = structlog.get_logger()

router = APIRouter()


@router.post("/project/{project_id}/images", response_model=dict)
async def upload_project_images(
    project_id: int = Path(..., description="ID del proyecto"),
    files: List[UploadFile] = File(..., description="Archivos de imagen"),
    image_type: str = Query("general", description="Tipo de imagen"),
    alt_text: Optional[str] = Query(None, description="Texto alternativo"),
    is_featured: bool = Query(False, description="Marcar como imagen destacada"),
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Subir imágenes de proyecto a S3 y guardar en base de datos"""
    try:
        if not files or len(files) == 0:
            raise HTTPException(status_code=400, detail="Se requiere al menos un archivo de imagen")
        if len(files) > 10:
            raise HTTPException(status_code=400, detail="No se pueden subir más de 10 imágenes a la vez")
        
        for file in files:
            if not file.content_type or not file.content_type.startswith('image/'):
                raise HTTPException(status_code=400, detail=f"El archivo {file.filename} no es una imagen válida")
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:
                raise HTTPException(status_code=400, detail=f"La imagen {file.filename} es muy grande (máx 10MB)")
            await file.seek(0)
        
        project_image = await create_project_images(
            db=db, project_id=project_id, files=files,
            broker_email=current_user.email, image_type=image_type,
            alt_text=alt_text, is_featured=is_featured
        )
        
        urls_list = project_image.url.split(',') if project_image.url else []
        keys_list = [k for url in urls_list if (k := s3_service.extract_key_from_url(url))]
        
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
                "bucket": s3_service.bucket_name,
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
    _current_user: User = RequireAuth,
):
    """Obtener imágenes de un proyecto desde la base de datos"""
    try:
        images = await get_project_images(db=db, project_id=project_id, image_type=image_type, is_featured=is_featured)
        
        processed_images = []
        all_urls = []
        for image in images:
            urls = image.url.split(',') if image.url else []
            all_urls.extend(urls)
            processed_images.append({
                "id": image.id, "filename": image.filename,
                "url": urls[0] if urls else "",
                "image_type": image.image_type, "is_featured": image.is_featured,
                "is_active": image.is_active, "display_order": image.display_order,
                "alt_text": image.alt_text, "urls_list": urls,
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
    _current_user: User = RequireAuth,
):
    """Obtener resumen de imágenes del proyecto"""
    try:
        summary = await get_project_images_summary(db=db, project_id=project_id)
        return {"success": True, "message": f"Resumen de imágenes del proyecto {project_id}", "data": summary}
    except Exception as e:
        logger.error("Error obteniendo resumen de imágenes", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/project-image/{image_id}", response_model=dict)
async def update_project_image_endpoint(
    image_id: int = Path(..., description="ID de la imagen"),
    image_type: Optional[str] = Query(None, description="Tipo de imagen"),
    alt_text: Optional[str] = Query(None, description="Texto alternativo"),
    is_featured: Optional[bool] = Query(None, description="Marcar como destacada"),
    is_active: Optional[bool] = Query(None, description="Activar/desactivar imagen"),
    display_order: Optional[int] = Query(None, description="Orden de visualización"),
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Actualizar información de imagen de proyecto"""
    try:
        update_data = {}
        if image_type is not None: update_data["image_type"] = image_type
        if alt_text is not None: update_data["alt_text"] = alt_text
        if is_featured is not None: update_data["is_featured"] = is_featured
        if is_active is not None: update_data["is_active"] = is_active
        if display_order is not None: update_data["display_order"] = display_order
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Se requiere al menos un campo para actualizar")
        
        image = await update_project_image(db=db, image_id=image_id, update_data=update_data, broker_email=current_user.email)
        urls_list = image.url.split(',') if image.url else []
        
        return {
            "success": True, "message": "Imagen actualizada exitosamente",
            "data": {
                "id": image.id, "project_id": image.project_id,
                "filename": image.filename, "image_type": image.image_type,
                "is_featured": image.is_featured, "is_active": image.is_active,
                "display_order": image.display_order, "alt_text": image.alt_text,
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
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Eliminar imagen de proyecto (soft delete)"""
    try:
        await delete_project_image(db=db, image_id=image_id, broker_email=current_user.email)
        return {"success": True, "message": "Imagen eliminada exitosamente", "data": {"image_id": image_id, "deleted_at": "now"}}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error eliminando imagen de proyecto", image_id=image_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.post("/project/{project_id}/documents", response_model=dict)
async def upload_project_document(
    project_id: int = Path(..., description="ID del proyecto"),
    file: UploadFile = File(..., description="Archivo de documento"),
    document_type: str = Query("general", description="Tipo de documento"),
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Subir documento de proyecto a S3 y guardar en base de datos"""
    try:
        allowed_types = [
            'application/pdf', 'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'text/plain',
            'text/csv',
            'application/csv',
        ]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Tipo de archivo no permitido. Solo: PDF, DOC, DOCX, XLS, XLSX, TXT, CSV")
        
        content = await file.read()
        if len(content) > 25 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="El archivo no puede ser mayor a 25MB")
        await file.seek(0)
        
        project_document = await create_project_document(
            db=db, project_id=project_id, file=file,
            broker_email=current_user.email, document_type=document_type
        )
        
        return {
            "success": True, "message": "Documento subido exitosamente",
            "data": {
                "document_id": project_document.id, "project_id": project_id,
                "filename": project_document.filename, "url": project_document.url,
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
    _current_user: User = RequireAuth,
):
    """Obtener documentos de un proyecto desde la base de datos"""
    try:
        documents = await get_project_documents(db=db, project_id=project_id, document_type=document_type)
        processed_documents = [{
            "id": doc.id, "filename": doc.filename, "url": doc.url,
            "document_type": doc.document_type, "is_active": doc.is_active,
            "created_at": doc.created_at.isoformat() if doc.created_at else None
        } for doc in documents]
        
        return {
            "success": True,
            "message": f"Documentos del proyecto {project_id} desde base de datos",
            "data": {"project_id": project_id, "total_documents": len(documents), "documents": processed_documents}
        }
    except Exception as e:
        logger.error("Error obteniendo documentos de proyecto", project_id=project_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")


@router.put("/project-document/{document_id}", response_model=dict)
async def update_project_document_endpoint(
    document_id: int = Path(..., description="ID del documento"),
    document_type: Optional[str] = Query(None, description="Tipo de documento"),
    is_active: Optional[bool] = Query(None, description="Activar/desactivar documento"),
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Actualizar información de documento de proyecto"""
    try:
        update_data = {}
        if document_type is not None: update_data["document_type"] = document_type
        if is_active is not None: update_data["is_active"] = is_active
        
        if not update_data:
            raise HTTPException(status_code=400, detail="Se requiere al menos un campo para actualizar")
        
        document = await update_project_document(db=db, document_id=document_id, update_data=update_data, broker_email=current_user.email)
        
        return {
            "success": True, "message": "Documento actualizado exitosamente",
            "data": {
                "id": document.id, "project_id": document.project_id,
                "filename": document.filename, "url": document.url,
                "document_type": document.document_type, "is_active": document.is_active,
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
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Eliminar documento de proyecto (soft delete)"""
    try:
        await delete_project_document(db=db, document_id=document_id, broker_email=current_user.email)
        return {"success": True, "message": "Documento eliminado exitosamente", "data": {"document_id": document_id, "deleted_at": "now"}}
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error eliminando documento de proyecto", document_id=document_id, error=str(e))
        raise HTTPException(status_code=500, detail="Error interno del servidor")
