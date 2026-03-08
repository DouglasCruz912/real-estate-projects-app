"""
Router para gestión de stock de propiedades
CRUD completo con autenticación JWT
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies.db_dependencies import DatabaseDep
from ..dependencies.auth_dependencies import RequireAuth
from ..services import stock_service
from ..utils.exceptions import APIException, StockUnitNotFoundError, ValidationError
from ..schemas.stock import (
    StockCreateRequest,
    StockUpdateRequest,
    StockResponse,
    StockListResponse
)
from ..models import User

router = APIRouter()


@router.post("", response_model=StockResponse, status_code=201)
async def create_stock(
    stock_data: StockCreateRequest,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Crear una nueva unidad de stock"""
    try:
        project_id = stock_data.project_id
        stock_dict = stock_data.model_dump(exclude_unset=True, exclude={'project_id'})
        
        stock = await stock_service.create_stock_unit(
            db=db, project_id=project_id,
            stock_data=stock_dict, broker_email=current_user.email
        )
        return StockResponse.model_validate(stock)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/{stock_id}", response_model=StockResponse)
async def get_stock_unit(
    stock_id: int,
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Obtener una unidad de stock específica por ID"""
    try:
        stock = await stock_service.get_stock_by_id(db=db, stock_id=stock_id)
        return StockResponse.model_validate(stock)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.put("/{stock_id}", response_model=StockResponse)
async def update_stock(
    stock_id: int,
    update_data: StockUpdateRequest,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Actualizar una unidad de stock existente"""
    try:
        stock = await stock_service.update_stock_unit(
            db=db, stock_id=stock_id,
            update_data=update_data.model_dump(exclude_unset=True),
            broker_email=current_user.email
        )
        return StockResponse.model_validate(stock)
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.delete("/{stock_id}", status_code=200)
async def delete_stock(
    stock_id: int,
    db: AsyncSession = DatabaseDep,
    current_user: User = RequireAuth,
):
    """Eliminar una unidad de stock (soft delete)"""
    try:
        result = await stock_service.delete_stock_unit(db=db, stock_id=stock_id, broker_email=current_user.email)
        return result
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@router.get("/project/{project_id}")
async def get_stock_by_project(
    project_id: int,
    skip: int = Query(0, ge=0, description="Número de registros a omitir"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
    available_only: bool = Query(False, description="Solo unidades disponibles"),
    db: AsyncSession = DatabaseDep,
    _current_user: User = RequireAuth,
):
    """Obtener stock de un proyecto específico"""
    try:
        stock, total = await stock_service.get_stock_by_project(
            db=db, project_id=project_id,
            skip=skip, limit=limit, available_only=available_only
        )
        return StockListResponse(
            stock=[StockResponse.model_validate(unit) for unit in stock],
            total=total, page=(skip // limit) + 1,
            per_page=limit, total_pages=(total + limit - 1) // limit
        )
    except APIException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
