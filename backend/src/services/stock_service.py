"""
Servicio de negocio para Stock de Proyectos
Lógica de CRUD con validaciones de estado
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc, case
from decimal import Decimal
import structlog
from datetime import date

from ..models import ProjectStock, Project
from ..utils.exceptions import (
    APIException,
    StockUnitNotFoundError,
    ProjectNotFoundError,
    InvalidStockStatusError,
    StockNotAvailableError,
    ValidationError,
    DatabaseError
)
from . import user_service
from .project_service import update_project_aggregates

logger = structlog.get_logger()


async def create_stock_unit(
    db: AsyncSession,
    project_id: int,
    stock_data: Dict[str, Any],
    broker_email: str
) -> ProjectStock:
    """Crear nueva unidad de stock"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Validar que el proyecto existe
        await _validate_project_exists(db, project_id)
        
        # Validar número de unidad único en el proyecto
        await _validate_unique_unit_number(db, project_id, stock_data['unit_number'])
        
        # Crear unidad de stock
        stock_unit = ProjectStock(
            project_id=project_id,
            **stock_data,
            created_by=user_id
        )
        
        db.add(stock_unit)
        await db.commit()
        await db.refresh(stock_unit)

        await update_project_aggregates(db, project_id)

        logger.info(
            "Unidad de stock creada",
            stock_id=stock_unit.id,
            project_id=project_id,
            unit_number=stock_unit.unit_number,
            created_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return stock_unit
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error creando unidad de stock", error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_stock_by_id(
    db: AsyncSession,
    stock_id: int,
    include_project: bool = False
) -> ProjectStock:
    """Obtener unidad de stock por ID"""
    
    try:
        query = select(ProjectStock).where(
            and_(
                ProjectStock.id == stock_id,
                ProjectStock.deleted_at.is_(None)
            )
        )
        
        if include_project:
            from sqlalchemy.orm import selectinload
            query = query.options(selectinload(ProjectStock.project))
        
        result = await db.execute(query)
        stock_unit = result.scalar_one_or_none()
        
        if not stock_unit:
            raise StockUnitNotFoundError(stock_id)
        
        return stock_unit
        
    except StockUnitNotFoundError:
        raise
    except Exception as e:
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error obteniendo unidad de stock", stock_id=stock_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_project_stock_list(
    db: AsyncSession,
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    unit_type: Optional[str] = None,
    status: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    min_area: Optional[Decimal] = None,
    max_area: Optional[Decimal] = None,
    floor: Optional[int] = None,
    building: Optional[str] = None,
    has_parking: Optional[bool] = None,
    has_storage: Optional[bool] = None,
    only_available: bool = False
) -> List[ProjectStock]:
    """Obtener lista de stock del proyecto con filtros"""
    
    try:
        # Validar que el proyecto existe
        await _validate_project_exists(db, project_id)
        
        query = select(ProjectStock).where(
            and_(
                ProjectStock.project_id == project_id,
                ProjectStock.deleted_at.is_(None)
            )
        )
        
        # Aplicar filtros
        if only_available:
            query = query.where(ProjectStock.status == "available")
        
        if unit_type:
            query = query.where(ProjectStock.unit_type == unit_type)
        
        if status:
            query = query.where(ProjectStock.status == status)
        
        if bedrooms is not None:
            query = query.where(ProjectStock.bedrooms == bedrooms)
        
        if bathrooms is not None:
            query = query.where(ProjectStock.bathrooms == bathrooms)
        
        if min_price is not None:
            query = query.where(ProjectStock.value_base >= min_price)
        
        if max_price is not None:
            query = query.where(ProjectStock.value_base <= max_price)
        
        if min_area is not None:
            query = query.where(ProjectStock.total_area >= min_area)
        
        if max_area is not None:
            query = query.where(ProjectStock.total_area <= max_area)
        
        if floor is not None:
            query = query.where(ProjectStock.floor == floor)
        
        if building:
            query = query.where(ProjectStock.building.ilike(f"%{building}%"))
        
        if has_parking is not None:
            query = query.where(ProjectStock.has_parking == has_parking)
        
        if has_storage is not None:
            query = query.where(ProjectStock.has_storage == has_storage)
        
        # Ordenamiento y paginación
        query = query.order_by(
            case((ProjectStock.status == "available", 1), else_=0).desc(),
            ProjectStock.unit_number
        ).offset(skip).limit(limit)
        
        result = await db.execute(query)
        stock_units = result.scalars().all()
        
        return list(stock_units)
        
    except Exception as e:
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error listando stock del proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def update_stock_unit(
    db: AsyncSession,
    stock_id: int,
    update_data: Dict[str, Any],
    broker_email: str
) -> ProjectStock:
    """Actualizar unidad de stock"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        stock_unit = await get_stock_by_id(db, stock_id)
        
        # Validar número de unidad único si se está actualizando
        if 'unit_number' in update_data and update_data['unit_number'] != stock_unit.unit_number:
            await _validate_unique_unit_number(
                db, 
                stock_unit.project_id, 
                update_data['unit_number'],
                exclude_id=stock_id
            )
        
        # Validar cambios de estado
        if 'status' in update_data:
            await _validate_status_change(stock_unit, update_data['status'])
        
        # Actualizar campos
        for field, value in update_data.items():
            if hasattr(stock_unit, field):
                setattr(stock_unit, field, value)
        
        stock_unit.updated_by = user_id
        
        await db.commit()
        await db.refresh(stock_unit)

        await update_project_aggregates(db, stock_unit.project_id)

        logger.info(
            "Unidad de stock actualizada",
            stock_id=stock_unit.id,
            unit_number=stock_unit.unit_number,
            updated_fields=list(update_data.keys()),
            updated_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return stock_unit
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error actualizando stock", stock_id=stock_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")











async def delete_stock_unit(
    db: AsyncSession,
    stock_id: int,
    broker_email: str
) -> bool:
    """Eliminar unidad de stock (soft delete)"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        stock_unit = await get_stock_by_id(db, stock_id)
        
        # Validar que no está vendida
        if stock_unit.status == "sold":
            raise ValidationError("No se puede eliminar una unidad vendida")
        
        # Soft delete manual
        stock_unit.deleted_at = func.now()
        stock_unit.deleted_by = user_id
        stock_unit.updated_by = user_id
        
        await db.commit()

        await update_project_aggregates(db, stock_unit.project_id)

        logger.info(
            "Unidad de stock eliminada",
            stock_id=stock_unit.id,
            unit_number=stock_unit.unit_number,
            deleted_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return {
            "message": f"Unidad '{stock_unit.unit_number}' eliminada exitosamente",
            "stock_id": stock_unit.id,
            "project_id": stock_unit.project_id
        }
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error eliminando stock", stock_id=stock_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")





# Funciones auxiliares privadas
async def _validate_project_exists(db: AsyncSession, project_id: int) -> None:
    """Validar que el proyecto existe"""
    
    query = select(Project).where(
        and_(
            Project.id == project_id,
            Project.deleted_at.is_(None)
        )
    )
    
    project = await db.scalar(query)
    if not project:
        raise ProjectNotFoundError(project_id)


async def _validate_unique_unit_number(
    db: AsyncSession,
    project_id: int,
    unit_number: str,
    exclude_id: Optional[int] = None
) -> None:
    """Validar que el número de unidad es único en el proyecto"""
    
    query = select(ProjectStock).where(
        and_(
            ProjectStock.project_id == project_id,
            ProjectStock.unit_number == unit_number,
            ProjectStock.deleted_at.is_(None)
        )
    )
    
    if exclude_id:
        query = query.where(ProjectStock.id != exclude_id)
    
    existing = await db.scalar(query)
    if existing:
        raise ValidationError(f"El número de unidad '{unit_number}' ya existe en este proyecto")


async def _validate_status_change(stock_unit: ProjectStock, new_status: str) -> None:
    """Validar cambio de estado"""
    
    current_status = stock_unit.status
    
    # Si el estado no cambia, permitir la actualización
    if current_status == new_status:
        return
    
    # Definir transiciones válidas solo para cambios de estado
    valid_transitions = {
        "available": ["reserved", "sold", "blocked"],
        "reserved": ["available", "sold"],
        "sold": [],  # No se puede cambiar desde vendido
        "blocked": ["available"]
    }
    
    allowed_statuses = valid_transitions.get(current_status, [])
    
    if new_status not in allowed_statuses:
        raise InvalidStockStatusError(f"No se puede cambiar de '{current_status}' a '{new_status}'")



async def get_stock_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    project_id: Optional[int] = None,
    property_type: Optional[str] = None,
    state: Optional[str] = None,
    bedrooms: Optional[int] = None,
    bathrooms: Optional[int] = None,
    price_min: Optional[Decimal] = None,
    price_max: Optional[Decimal] = None,
    currency: Optional[str] = None,
    area_min: Optional[Decimal] = None,
    area_max: Optional[Decimal] = None,
    available_only: bool = False
) -> tuple[List[ProjectStock], int]:
    """Obtener lista de stock con filtros - función simplificada"""
    
    try:
        query = select(ProjectStock).where(ProjectStock.deleted_at.is_(None))
        
        # Aplicar filtros
        if project_id:
            query = query.where(ProjectStock.project_id == project_id)
        
        if available_only:
            query = query.where(ProjectStock.status == "available")
        
        if state:
            query = query.where(ProjectStock.status == state)
        
        if bedrooms is not None:
            query = query.where(ProjectStock.bedrooms == bedrooms)
        
        if bathrooms is not None:
            query = query.where(ProjectStock.bathrooms == bathrooms)
        
        if price_min is not None:
            query = query.where(ProjectStock.value_base >= price_min)
        
        if price_max is not None:
            query = query.where(ProjectStock.value_base <= price_max)
        
        if area_min is not None:
            query = query.where(ProjectStock.total_area >= area_min)
        
        if area_max is not None:
            query = query.where(ProjectStock.total_area <= area_max)
        
        # Contar total
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        # Aplicar paginación
        query = query.order_by(ProjectStock.unit_number).offset(skip).limit(limit)
        
        result = await db.execute(query)
        stock_units = result.scalars().all()
        
        return list(stock_units), total
        
    except Exception as e:
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error listando stock", error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")





async def get_stock_by_project(
    db: AsyncSession,
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    available_only: bool = False
) -> tuple[List[ProjectStock], int]:
    """Obtener stock de un proyecto - función simplificada"""
    
    try:
        query = select(ProjectStock).where(
            and_(
                ProjectStock.project_id == project_id,
                ProjectStock.deleted_at.is_(None)
            )
        )
        
        if available_only:
            query = query.where(ProjectStock.status == "available")
        
        # Contar total
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        # Aplicar paginación
        query = query.order_by(ProjectStock.unit_number).offset(skip).limit(limit)
        
        result = await db.execute(query)
        stock_units = result.scalars().all()
        
        return list(stock_units), total
        
    except Exception as e:
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error obteniendo stock del proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")














# Funciones auxiliares privadas 
