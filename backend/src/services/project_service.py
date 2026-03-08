"""
Servicio de negocio para Proyectos
Lógica de CRUD con desnormalización y cache
"""

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc, update, case
from sqlalchemy.orm import selectinload
from decimal import Decimal
import structlog

from ..models import (
    Project, RealEstateCompany, ProjectStock, 
    ProjectImage, LegalUser, ProjectCommercial, ProjectDocument
)
from ..utils.exceptions import (
    APIException,
    ProjectNotFoundError, 
    CompanyNotFoundError,
    DuplicateProjectError,
    ValidationError,
    DatabaseError
)
from . import user_service

logger = structlog.get_logger()



async def get_project_by_id(
    db: AsyncSession,
    project_id: int,
    include_relations: bool = False
) -> Project:
    """Obtener proyecto por ID con información comercial"""
    
    try:
        query = select(Project).where(
            and_(
                Project.id == project_id,
                Project.deleted_at.is_(None)
            )
        )
        
        if include_relations:
            query = query.options(
                selectinload(Project.company),
                selectinload(Project.images),
                selectinload(Project.legal_users),
                selectinload(Project.stock_units)
            )
        
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise ProjectNotFoundError(project_id)
        
        # Cargar información comercial (siempre)
        commercial = await db.scalar(
            select(ProjectCommercial).where(
                and_(
                    ProjectCommercial.project_id == project_id,
                    ProjectCommercial.deleted_at.is_(None)
                )
            )
        )
        
        # Asignar los datos comerciales al proyecto
        project.commercial = commercial
        
        return project
        
    except ProjectNotFoundError:
        raise
    except Exception as e:
        # Re-lanzar errores de API/negocio sin modificar
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error obteniendo proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_projects_list(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    company_id: Optional[int] = None,
    state: Optional[str] = None,
    location: Optional[str] = None,
    price_min: Optional[Decimal] = None,
    price_max: Optional[Decimal] = None,
    currency: Optional[str] = None,
    available_only: bool = False
) -> tuple[List[Project], int]:
    """Obtener lista de proyectos con filtros"""
    
    try:
        query = select(Project).where(
            Project.deleted_at.is_(None)
        )
        
        # Aplicar filtros
        if company_id:
            query = query.where(Project.company_id == company_id)
        
        if state:
            query = query.where(Project.state == state)
        
        if location:
            query = query.where(
                or_(
                    Project.city.ilike(f"%{location}%"),
                    Project.region.ilike(f"%{location}%"),
                    Project.address.ilike(f"%{location}%")
                )
            )
        
        if price_min is not None:
            query = query.where(Project.price_from >= price_min)
        
        if price_max is not None:
            query = query.where(Project.price_to <= price_max)
        
        if currency:
            query = query.where(Project.currency == currency)
        
        if available_only:
            query = query.where(Project.available_units > 0)
        
        # Contar total antes de aplicar paginación
        count_query = select(func.count()).select_from(query.subquery())
        total = await db.scalar(count_query)
        
        # Ordenamiento y paginación
        query = query.order_by(
            desc(Project.created_at),
            Project.name
        ).offset(skip).limit(limit)
        
        result = await db.execute(query)
        projects = result.scalars().all()
        
        # Cargar información comercial para cada proyecto
        projects_with_commercial = []
        for project in projects:
            # Cargar información comercial
            commercial = await db.scalar(
                select(ProjectCommercial).where(
                    and_(
                        ProjectCommercial.project_id == project.id,
                        ProjectCommercial.deleted_at.is_(None)
                    )
                )
            )
            
            # Asignar los datos comerciales al proyecto
            project.commercial = commercial
            projects_with_commercial.append(project)
        
        return projects_with_commercial, total or 0
        
    except Exception as e:
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error listando proyectos", error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def update_project(
    db: AsyncSession,
    project_id: int,
    update_data: Dict[str, Any],
    broker_email: str
) -> Project:
    """Actualizar proyecto con información comercial"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        project = await get_project_by_id(db, project_id)
        
        # Separar datos del proyecto de datos comerciales
        project_fields, commercial_fields = _separate_project_and_commercial_data(update_data)
        
        # Validar campos únicos si se están actualizando
        unique_fields = ['slug']
        for field in unique_fields:
            if field in project_fields and project_fields[field] != getattr(project, field):
                await _validate_unique_project_fields(
                    db, 
                    {field: project_fields[field]}, 
                    exclude_id=project_id
                )
        
        # Si se cambia la compañía, actualizar datos desnormalizados
        if 'company_id' in project_fields and project_fields['company_id'] != project.company_id:
            company = await _get_company_for_denormalization(db, project_fields['company_id'])
            project_fields['company_name'] = company.name
        
        # Actualizar campos del proyecto
        for field, value in project_fields.items():
            if hasattr(project, field):
                setattr(project, field, value)
        
        project.updated_by = user_id
        
        await db.commit()
        await db.refresh(project)
        
        # Actualizar información comercial si hay datos comerciales
        commercial = None
        if commercial_fields and any(v is not None for v in commercial_fields.values()):
            # Buscar registro comercial existente
            commercial = await db.scalar(
                select(ProjectCommercial).where(
                    and_(
                        ProjectCommercial.project_id == project_id,
                        ProjectCommercial.deleted_at.is_(None)
                    )
                )
            )
            
            if commercial:
                # Actualizar registro existente
                for field, value in commercial_fields.items():
                    if hasattr(commercial, field):
                        setattr(commercial, field, value)
                commercial.updated_by = user_id
                
                await db.commit()
                await db.refresh(commercial)
                
                logger.info(
                    "Información comercial actualizada",
                    commercial_id=commercial.id,
                    project_id=project_id
                )
            else:
                # Crear nuevo registro comercial
                commercial = ProjectCommercial(
                    project_id=project_id,
                    created_by=user_id,
                    **commercial_fields
                )
                
                db.add(commercial)
                await db.commit()
                await db.refresh(commercial)
                
                logger.info(
                    "Información comercial creada",
                    commercial_id=commercial.id,
                    project_id=project_id
                )
        
        # Cargar la información comercial en el proyecto para la respuesta
        if not commercial:
            commercial = await db.scalar(
                select(ProjectCommercial).where(
                    and_(
                        ProjectCommercial.project_id == project_id,
                        ProjectCommercial.deleted_at.is_(None)
                    )
                )
            )
        
        project.commercial = commercial
        
        logger.info(
            "Proyecto actualizado",
            project_id=project.id,
            updated_project_fields=list(project_fields.keys()),
            updated_commercial_fields=list(commercial_fields.keys()),
            has_commercial=commercial is not None,
            updated_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return project
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error actualizando proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def delete_project(
    db: AsyncSession,
    project_id: int,
    broker_email: str
) -> bool:
    """Eliminar proyecto (soft delete)"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        project = await get_project_by_id(db, project_id)
        
        # Verificar si tiene stock vendido
        if hasattr(project, 'sold_stock_units') and project.sold_stock_units > 0:
            raise ValidationError(
                f"No se puede eliminar el proyecto. Tiene {project.sold_stock_units} unidades vendidas."
            )
        
        project.deleted_at = func.now()
        project.deleted_by = user_id
        project.updated_by = user_id
        
        await db.commit()
        
        logger.info(
            "Proyecto eliminado",
            project_id=project.id,
            deleted_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return {
            "message": f"Proyecto '{project.name}' eliminado exitosamente",
            "project_id": project.id,
            "project_name": project.name
        }
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error eliminando proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")





async def update_project_aggregates(
    db: AsyncSession,
    project_id: int
) -> None:
    """Actualizar campos agregados del proyecto desde stock"""
    
    try:
        # Calcular agregaciones desde stock - usar sintaxis compatible con MySQL
        stock_query = select(
            func.count(ProjectStock.id).label('total'),
            func.sum(case((ProjectStock.status == "available", 1), else_=0)).label('available'),
            func.sum(case((ProjectStock.status == "reserved", 1), else_=0)).label('reserved'),
            func.sum(case((ProjectStock.status == "sold", 1), else_=0)).label('sold'),
            func.min(ProjectStock.value_base).label('min_price'),
            func.max(ProjectStock.value_base).label('max_price'),
            func.min(ProjectStock.total_area).label('min_area'),
            func.max(ProjectStock.total_area).label('max_area'),
            func.min(ProjectStock.bedrooms).label('min_bedrooms'),
            func.max(ProjectStock.bedrooms).label('max_bedrooms'),
            func.min(ProjectStock.bathrooms).label('min_bathrooms'),
            func.max(ProjectStock.bathrooms).label('max_bathrooms')
        ).where(
            and_(
                ProjectStock.project_id == project_id,
                ProjectStock.deleted_at.is_(None)
            )
        )
        
        result = await db.execute(stock_query)
        row = result.first()
        
        # Actualizar proyecto
        update_query = update(Project).where(Project.id == project_id).values(
            total_units=row.total or 0,
            available_units=row.available or 0,
            price_from=row.min_price,
            price_to=row.max_price,
        )
        
        await db.execute(update_query)
        await db.commit()
        
        logger.info(
            "Agregaciones del proyecto actualizadas",
            project_id=project_id,
            total_units=row.total or 0
        )
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar (APIException incluye todas las excepciones personalizadas)
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error actualizando agregaciones", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


# Funciones auxiliares privadas
async def _validate_company_exists(db: AsyncSession, company_id: int) -> None:
    """Validar que la inmobiliaria existe"""
    
    query = select(RealEstateCompany).where(
        and_(
            RealEstateCompany.id == company_id,
            RealEstateCompany.deleted_at.is_(None),
            RealEstateCompany.is_active == True
        )
    )
    
    company = await db.scalar(query)
    if not company:
        raise CompanyNotFoundError(company_id)


async def _validate_unique_project_fields(
    db: AsyncSession,
    data: Dict[str, Any],
    exclude_id: Optional[int] = None
) -> None:
    """Validar campos únicos del proyecto"""
    
    if 'slug' in data and data['slug']:
        query = select(Project).where(
            and_(
                Project.slug == data['slug'],
                Project.deleted_at.is_(None)
            )
        )
        
        if exclude_id:
            query = query.where(Project.id != exclude_id)
        
        existing = await db.scalar(query)
        if existing:
            raise DuplicateProjectError(f"Slug '{data['slug']}' ya existe")


async def _get_company_for_denormalization(db: AsyncSession, company_id: int) -> RealEstateCompany:
    """Obtener datos de inmobiliaria para desnormalización"""
    
    query = select(RealEstateCompany).where(RealEstateCompany.id == company_id)
    company = await db.scalar(query)
    
    if not company:
        raise CompanyNotFoundError(company_id)
    
    return company


def _separate_project_and_commercial_data(data: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """Separar campos del proyecto de campos comerciales"""
    
    # Campos que van a la tabla project_commercial
    commercial_fields = {
        # Información de Postventa
        'after_sales_email', 'after_sales_executive', 'after_sales_phone',
        # Información Financiera  
        'finances_insurance_company', 'finances_insurance_policy', 'finances_insured_value',
        'finances_insured_value_util', 'finances_benefit', 'finances_annual_rate', 'finances_credit_rate',
        # Información Comercial Variable
        'down_payment_bonus', 'reservation', 'pre_approval', 'installments', 'balloon_payment',
        'annual_capital_gain', 'construction_capital_gain', 'vacancy', 'additional_information',
        'initial_payment', 'big_down_payment', 'notes_rent',
        # Campos JSON Flexibles
        'social_networks', 'payment_plan_conditions', 'promotions_benefits', 'frequently_asked_questions'
    }
    
    # Separar los datos
    project_data = {}
    commercial_data = {}
    
    for key, value in data.items():
        if key in commercial_fields:
            commercial_data[key] = value
        else:
            project_data[key] = value
    
    return project_data, commercial_data


def _combine_project_and_commercial_data(project: Project) -> Dict[str, Any]:
    """Combinar datos del proyecto con datos comerciales para la respuesta"""
    
    # Convertir el proyecto a diccionario (campos básicos)
    project_dict = {
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'company_id': project.company_id,
        'executive': project.executive,
        'executive_email': project.executive_email,
        
        # Ubicación
        'city': project.city,
        'region': project.region,
        'address': project.address,
        'street_number': project.street_number,
        'commune': project.commune,
        'country': project.country,
        'postal_code': project.postal_code,
        'url_google_maps': project.url_google_maps,
        'latitude': project.latitude,
        'longitude': project.longitude,
        
        # Contacto
        'phone': project.phone,
        'website': project.website,
        
        # Fechas
        'start_date': project.start_date,
        'delivery_date': project.delivery_date,
        'delivery_end_date': project.delivery_end_date,
        'launch_date': project.launch_date,
        
        # Unidades y precios
        'total_units': project.total_units,
        'available_units': project.available_units,
        'price_from': project.price_from,
        'price_to': project.price_to,
        'unique_price': project.unique_price,
        'currency': project.currency,
        
        # Tipo de proyecto
        'type': project.type,
        'delivery_type': project.delivery_type,
        
        # Estado
        'state': project.state,
        'is_active': project.is_active,
        'is_published': project.is_published,
        'is_promo': project.is_promo,
        'is_hot': project.is_hot,
        'created_at': project.created_at,
        'updated_at': project.updated_at,
    }
    
    # Agregar datos comerciales si existen
    if hasattr(project, 'commercial') and project.commercial:
        commercial = project.commercial
        project_dict.update({
            # Información de Postventa
            'after_sales_email': commercial.after_sales_email,
            'after_sales_executive': commercial.after_sales_executive,
            'after_sales_phone': commercial.after_sales_phone,
            
            # Información Financiera
            'finances_insurance_company': commercial.finances_insurance_company,
            'finances_insurance_policy': commercial.finances_insurance_policy,
            'finances_insured_value': commercial.finances_insured_value,
            'finances_insured_value_util': commercial.finances_insured_value_util,
            'finances_benefit': commercial.finances_benefit,
            'finances_annual_rate': commercial.finances_annual_rate,
            'finances_credit_rate': commercial.finances_credit_rate,
            
            # Información Comercial Variable
            'down_payment_bonus': commercial.down_payment_bonus,
            'reservation': commercial.reservation,
            'pre_approval': commercial.pre_approval,
            'installments': commercial.installments,
            'balloon_payment': commercial.balloon_payment,
            'annual_capital_gain': commercial.annual_capital_gain,
            'construction_capital_gain': commercial.construction_capital_gain,
            'vacancy': commercial.vacancy,
            'additional_information': commercial.additional_information,
            'initial_payment': commercial.initial_payment,
            'big_down_payment': commercial.big_down_payment,
            'notes_rent': commercial.notes_rent,
            
            # Campos JSON Flexibles
            'social_networks': commercial.social_networks,
            'payment_plan_conditions': commercial.payment_plan_conditions,
            'promotions_benefits': commercial.promotions_benefits,
            'frequently_asked_questions': commercial.frequently_asked_questions,
        })
    else:
        # Si no hay datos comerciales, agregar campos como None
        commercial_fields = [
            'after_sales_email', 'after_sales_executive', 'after_sales_phone',
            'finances_insurance_company', 'finances_insurance_policy', 'finances_insured_value',
            'finances_insured_value_util', 'finances_benefit', 'finances_annual_rate', 'finances_credit_rate',
            'down_payment_bonus', 'reservation', 'pre_approval', 'installments', 'balloon_payment',
            'annual_capital_gain', 'construction_capital_gain', 'vacancy', 'additional_information',
            'initial_payment', 'big_down_payment', 'notes_rent',
            'social_networks', 'payment_plan_conditions', 'promotions_benefits', 'frequently_asked_questions'
        ]
        
        for field in commercial_fields:
            project_dict[field] = None
    
    return project_dict





# Al final del archivo, agregar las funciones faltantes

async def create_project(
    db: AsyncSession,
    project_data: Dict[str, Any],
    broker_email: str
) -> Project:
    """Crear nuevo proyecto con información comercial opcional"""
    
    try:
        # Obtener user_id del broker por email
        user_id = await user_service.get_user_id_by_email(db, broker_email)
        
        # Validar que la inmobiliaria existe
        await _validate_company_exists(db, project_data['company_id'])
        
        # Separar datos del proyecto de datos comerciales
        project_fields, commercial_fields = _separate_project_and_commercial_data(project_data)
        
        project = Project(
            **project_fields,
            created_by=user_id,
            total_units=0,       # Siempre inicia en 0
            available_units=0    # Siempre inicia en 0
        )
        
        db.add(project)
        await db.commit()
        await db.refresh(project)
        
        # Si hay datos comerciales, crear registro comercial
        commercial = None
        if commercial_fields and any(v is not None for v in commercial_fields.values()):
            commercial = ProjectCommercial(
                project_id=project.id,
                created_by=user_id,
                **commercial_fields
            )
            
            db.add(commercial)
            await db.commit()
            await db.refresh(commercial)
            
            logger.info(
                "Información comercial creada", 
                commercial_id=commercial.id,
                project_id=project.id
            )
        
        # Cargar la información comercial en el proyecto para la respuesta
        project.commercial = commercial
        
        logger.info(
            "Proyecto creado", 
            project_id=project.id, 
            name=project.name,
            has_commercial=commercial is not None,
            created_by_user_id=user_id,
            broker_email=broker_email
        )
        
        return project
        
    except Exception as e:
        await db.rollback()
        # Re-lanzar errores de API/negocio sin modificar
        if isinstance(e, APIException):
            raise e
        # Para errores técnicos/de base de datos
        logger.error("Error creando proyecto", error=str(e))
        raise DatabaseError(f"Error técnico en operación de base de datos: {str(e)}")


async def get_full_project_details(db: AsyncSession, project_id: int) -> Project:
    """Obtener todos los detalles de un proyecto, incluyendo relaciones."""
    
    try:
        query = select(Project).where(
            and_(
                Project.id == project_id,
                Project.deleted_at.is_(None)
            )
        ).options(
            selectinload(Project.company),
            selectinload(Project.commercial),
            selectinload(Project.stock_units),
            selectinload(Project.images),
            selectinload(Project.documents)
        )
        
        result = await db.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            raise ProjectNotFoundError(project_id)
        
        # Filtrar registros eliminados (soft delete) de las relaciones cargadas
        if hasattr(project, 'stock_units') and project.stock_units:
            project.stock_units = [stock for stock in project.stock_units if stock.deleted_at is None]
        
        if hasattr(project, 'images') and project.images:
            project.images = [image for image in project.images if image.deleted_at is None]
        
        if hasattr(project, 'documents') and project.documents:
            project.documents = [doc for doc in project.documents if doc.deleted_at is None]
        
        if hasattr(project, 'commercial') and project.commercial and project.commercial.deleted_at is not None:
            project.commercial = None
            
        return project
        
    except ProjectNotFoundError:
        raise
    except Exception as e:
        logger.error("Error obteniendo detalles completos del proyecto", project_id=project_id, error=str(e))
        raise DatabaseError(f"Error técnico al obtener detalles del proyecto: {str(e)}")


# Nota: Las funciones comerciales separadas han sido eliminadas
# La lógica comercial ahora está integrada en create_project, update_project y get_project_by_id





