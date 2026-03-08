"""
Router FastAPI para Inmobiliarias
CRUD completo con autenticación JWT
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAuth
from ..services import company_service
from ..utils.exceptions import APIException
from ..schemas.companies import CompanyCreate, CompanyUpdate, CompanyResponse
from ..models import User

router = APIRouter()


@router.post("", response_model=CompanyResponse, status_code=201)
async def create_company(
    company_data: CompanyCreate,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Crear nueva inmobiliaria"""
    try:
        company = await company_service.create_company(
            db=db,
            company_data=company_data.model_dump(exclude_unset=True),
            broker_email=current_user.email
        )
        return CompanyResponse.model_validate(company)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("", response_model=List[CompanyResponse])
async def list_companies(
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    search: Optional[str] = Query(None, description="Buscar por nombre, razón social o RUT"),
    city: Optional[str] = Query(None, description="Filtrar por ciudad"),
    region: Optional[str] = Query(None, description="Filtrar por región"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    is_verified: Optional[bool] = Query(None, description="Filtrar por verificación"),
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Listar inmobiliarias con filtros"""
    try:
        companies = await company_service.get_companies_list(
            db=db, skip=skip, limit=limit, search=search,
            city=city, region=region, is_active=is_active, is_verified=is_verified
        )
        return [CompanyResponse.model_validate(company) for company in companies]
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Obtener inmobiliaria por ID"""
    try:
        company = await company_service.get_company_by_id(db=db, company_id=company_id, include_projects=False)
        return CompanyResponse.model_validate(company)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(
    company_id: int,
    update_data: CompanyUpdate,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Actualizar inmobiliaria"""
    try:
        company = await company_service.update_company(
            db=db, company_id=company_id,
            update_data=update_data.model_dump(exclude_unset=True),
            broker_email=current_user.email
        )
        return CompanyResponse.model_validate(company)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{company_id}", status_code=200)
async def delete_company(
    company_id: int,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Eliminar inmobiliaria (soft delete)"""
    try:
        result = await company_service.delete_company(db=db, company_id=company_id, broker_email=current_user.email)
        return result
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
