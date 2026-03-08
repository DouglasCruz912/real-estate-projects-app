"""
Servicio de negocio para Inmobiliarias
Lógica de CRUD y validaciones específicas con auditoría automática
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload
import structlog

from ..models import RealEstateCompany, Project
from ..utils.exceptions import (
    APIException,
    CompanyNotFoundError, 
    DuplicateCompanyError,
    ValidationError,
    DatabaseError
)
from . import user_service

logger = structlog.get_logger()


async def create_company(
    db: AsyncSession,
    company_data: Dict[str, Any],
    broker_email: str
) -> RealEstateCompany:
    """Crear nueva inmobiliaria"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Validar datos únicos
        await _validate_unique_fields(db, company_data)
        
        company = RealEstateCompany(
            **company_data,
            created_by=user_id
        )
        
        db.add(company)
        await db.commit()
        await db.refresh(company)
        
        logger.info(
            "Inmobiliaria creada",
            company_id=company.id,
            name=company.name,
            created_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return company
        
    except (APIException, CompanyNotFoundError, DuplicateCompanyError, ValidationError) as e:
        # Errores de negocio/API - dejar pasar sin modificar
        await db.rollback()
        raise
    except Exception as e:
        # Errores inesperados de BD - log y relanzar como DatabaseError
        await db.rollback()
        logger.error("Error inesperado creando inmobiliaria", error=str(e))
        raise DatabaseError(f"Error interno del servidor: {str(e)}")


async def get_company_by_id(
    db: AsyncSession,
    company_id: int,
    include_projects: bool = False
) -> RealEstateCompany:
    """Obtener inmobiliaria por ID"""
    
    try:
        query = select(RealEstateCompany).where(
            and_(
                RealEstateCompany.id == company_id,
                RealEstateCompany.deleted_at.is_(None)
            )
        )
        
        if include_projects:
            query = query.options(
                selectinload(RealEstateCompany.projects).selectinload(Project.stock_units)
            )
        
        result = await db.execute(query)
        company = result.scalar_one_or_none()
        
        if not company:
            raise CompanyNotFoundError(company_id)
        
        return company
        
    except CompanyNotFoundError:
        raise
    except Exception as e:
        logger.error("Error inesperado obteniendo inmobiliaria", company_id=company_id, error=str(e))
        raise DatabaseError(f"Error interno del servidor: {str(e)}")


async def get_companies_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    city: Optional[str] = None,
    region: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_verified: Optional[bool] = None
) -> List[RealEstateCompany]:
    """Obtener lista de inmobiliarias con filtros"""
    
    try:
        query = select(RealEstateCompany).where(
            RealEstateCompany.deleted_at.is_(None)
        )
        
        # Aplicar filtros
        if search:
            search_filter = or_(
                RealEstateCompany.name.ilike(f"%{search}%"),
                RealEstateCompany.legal_name.ilike(f"%{search}%"),
                RealEstateCompany.rut.ilike(f"%{search}%")
            )
            query = query.where(search_filter)
        
        if city:
            query = query.where(RealEstateCompany.city.ilike(f"%{city}%"))
        
        if region:
            query = query.where(RealEstateCompany.region.ilike(f"%{region}%"))
        
        if is_active is not None:
            query = query.where(RealEstateCompany.is_active == is_active)
        
        if is_verified is not None:
            query = query.where(RealEstateCompany.is_verified == is_verified)
        
        # Ordenar y paginar
        query = query.order_by(desc(RealEstateCompany.created_at))
        query = query.offset(skip).limit(limit)
        
        result = await db.execute(query)
        companies = result.scalars().all()
        
        return list(companies)
        
    except Exception as e:
        logger.error("Error listando inmobiliarias", error=str(e))
        raise DatabaseError(f"Error interno del servidor: {str(e)}")


async def update_company(
    db: AsyncSession,
    company_id: int,
    update_data: Dict[str, Any],
    broker_email: str
) -> RealEstateCompany:
    """Actualizar inmobiliaria"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Obtener company actual
        company = await get_company_by_id(db, company_id)
        
        # Validar datos únicos si se van a actualizar
        if any(field in update_data for field in ['rut', 'name']):
            await _validate_unique_fields(db, update_data, exclude_id=company_id)
        
        # Actualizar campos
        for field, value in update_data.items():
            if hasattr(company, field):
                setattr(company, field, value)
        
        # Auditoría
        company.updated_by = user_id
        
        await db.commit()
        await db.refresh(company)
        
        logger.info(
            "Inmobiliaria actualizada",
            company_id=company.id,
            updated_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return company
        
    except (CompanyNotFoundError, DuplicateCompanyError, ValidationError) as e:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Error actualizando inmobiliaria", company_id=company_id, error=str(e))
        raise DatabaseError(f"Error interno del servidor: {str(e)}")


async def delete_company(
    db: AsyncSession,
    company_id: int,
    broker_email: str
) -> Dict[str, Any]:
    """Eliminar inmobiliaria (soft delete)"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Obtener company
        company = await get_company_by_id(db, company_id)
        
        # Verificar que no tenga proyectos activos
        active_projects_count = await _count_active_projects(db, company_id)
        if active_projects_count > 0:
            raise ValidationError(
                f"No se puede eliminar la inmobiliaria. Tiene {active_projects_count} proyectos activos"
            )
        
        # Soft delete y desactivar
        company.deleted_at = func.now()
        company.deleted_by = user_id
        company.is_active = False
        company.is_verified = False
        
        await db.commit()
        
        logger.info(
            "Inmobiliaria eliminada",
            company_id=company.id,
            deleted_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return {
            "message": f"Inmobiliaria '{company.name}' eliminada exitosamente",
            "company_id": company.id,
            "company_name": company.name
        }
        
    except (CompanyNotFoundError, ValidationError) as e:
        await db.rollback()
        raise
    except Exception as e:
        await db.rollback()
        logger.error("Error eliminando inmobiliaria", company_id=company_id, error=str(e))
        raise DatabaseError(f"Error interno del servidor: {str(e)}")





async def _validate_unique_fields(
    db: AsyncSession,
    data: Dict[str, Any],
    exclude_id: Optional[int] = None
) -> None:
    """Validar campos únicos"""
    
    if 'rut' in data and data['rut']:
        query = select(RealEstateCompany).where(
            and_(
                RealEstateCompany.rut == data['rut'],
                RealEstateCompany.deleted_at.is_(None)
            )
        )
        
        if exclude_id:
            query = query.where(RealEstateCompany.id != exclude_id)
        
        existing = await db.scalar(query)
        if existing:
            raise DuplicateCompanyError(f"RUT {data['rut']} ya existe")


async def _count_active_projects(db: AsyncSession, company_id: int) -> int:
    """Contar proyectos activos de la inmobiliaria"""
    
    query = select(func.count(Project.id)).where(
        and_(
            Project.company_id == company_id,
            Project.is_active == True,
            Project.deleted_at.is_(None)
        )
    )
    
    result = await db.scalar(query)
    return result or 0


