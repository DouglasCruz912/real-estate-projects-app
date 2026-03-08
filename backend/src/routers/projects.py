"""
Router para gestión de proyectos inmobiliarios
CRUD completo con autenticación JWT
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from decimal import Decimal

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAuth
from ..services import project_service
from ..utils.exceptions import APIException, ProjectNotFoundError, ValidationError
from ..schemas.projects import (
    ProjectCreateRequest, 
    ProjectUpdateRequest, 
    ProjectResponse, 
    ProjectListResponse,
    ProjectDetailsResponse
)
from ..models import User

router = APIRouter()


@router.post("", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreateRequest,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Crear un nuevo proyecto inmobiliario"""
    try:
        project = await project_service.create_project(
            db=db,
            project_data=project_data.model_dump(exclude_unset=True),
            broker_email=current_user.email
        )
        project_data_response = project_service._combine_project_and_commercial_data(project)
        return ProjectResponse(**project_data_response)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("", response_model=ProjectListResponse)
async def get_projects(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    company_id: Optional[int] = Query(None, ge=1, description="Filtrar por inmobiliaria"),
    state: Optional[str] = Query(None, description="Filtrar por estado"),
    location: Optional[str] = Query(None, description="Filtrar por ubicación"),
    price_min: Optional[Decimal] = Query(None, ge=0, description="Precio mínimo"),
    price_max: Optional[Decimal] = Query(None, ge=0, description="Precio máximo"),
    currency: Optional[str] = Query(None, description="Filtrar por moneda"),
    available_only: bool = Query(False, description="Solo proyectos con unidades disponibles"),
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Obtener lista de proyectos con filtros opcionales"""
    try:
        projects, total = await project_service.get_projects_list(
            db=db, skip=skip, limit=limit, company_id=company_id,
            state=state, location=location, price_min=price_min,
            price_max=price_max, currency=currency, available_only=available_only
        )
        
        projects_with_commercial = []
        for project in projects:
            project_data = project_service._combine_project_and_commercial_data(project)
            projects_with_commercial.append(ProjectResponse(**project_data))

        return ProjectListResponse(
            projects=projects_with_commercial, total=total,
            page=(skip // limit) + 1, per_page=limit,
            total_pages=(total + limit - 1) // limit
        )
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Obtener un proyecto específico por ID con información comercial incluida"""
    try:
        project = await project_service.get_project_by_id(db=db, project_id=project_id)
        project_data = project_service._combine_project_and_commercial_data(project)
        return ProjectResponse(**project_data)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    update_data: ProjectUpdateRequest,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Actualizar un proyecto existente"""
    try:
        project = await project_service.update_project(
            db=db, project_id=project_id,
            update_data=update_data.model_dump(exclude_unset=True),
            broker_email=current_user.email
        )
        project_data = project_service._combine_project_and_commercial_data(project)
        return ProjectResponse(**project_data)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{project_id}", status_code=200)
async def delete_project(
    project_id: int,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Eliminar un proyecto (soft delete)"""
    try:
        result = await project_service.delete_project(db=db, project_id=project_id, broker_email=current_user.email)
        return result
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{project_id}/details", response_model=ProjectDetailsResponse)
async def get_project_details(
    project_id: int,
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Obtener todos los detalles de un proyecto en una sola llamada"""
    try:
        project = await project_service.get_full_project_details(db, project_id)
        return ProjectDetailsResponse(
            project=project, company=project.company,
            stock=project.stock_units, images=project.images,
            documents=project.documents
        )
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
