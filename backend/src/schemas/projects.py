"""
Schemas de Pydantic para Proyectos Inmobiliarios
Modelos de request/response para el CRUD de projects
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from decimal import Decimal
from datetime import date, datetime
from .base import BaseResponse
from ..utils.constants import PROJECT_STATES, CURRENCY_TYPES





class ProjectCreateRequest(BaseModel):
    """Schema para crear proyecto inmobiliario"""
    name: str = Field(..., min_length=1, max_length=200, description="Nombre del proyecto")
    description: Optional[Dict[str, Any]] = Field(None, description="Descripción del proyecto como JSON")
    company_id: int = Field(..., gt=0, description="ID de la inmobiliaria")
    
    # Información de gestión
    executive: Optional[str] = Field(None, max_length=255, description="Ejecutivo responsable del proyecto")
    executive_email: Optional[str] = Field(None, max_length=255, description="Email del ejecutivo responsable")
    
    # Ubicación
    city: Optional[str] = Field(None, max_length=100, description="Ciudad del proyecto")
    region: Optional[str] = Field(None, max_length=100, description="Región del proyecto")
    address: Optional[str] = Field(None, description="Dirección del proyecto")
    street_number: Optional[str] = Field(None, max_length=20, description="Número de calle/dirección")
    commune: Optional[str] = Field(None, max_length=100, description="Comuna del proyecto")
    country: Optional[str] = Field(None, max_length=100, description="País donde se ubica el proyecto")
    postal_code: Optional[str] = Field(None, max_length=20, description="Código postal")
    url_google_maps: Optional[str] = Field(None, max_length=500, description="URL de ubicación en Google Maps")
    latitude: Optional[str] = Field(None, max_length=50, description="Coordenada GPS de latitud")
    longitude: Optional[str] = Field(None, max_length=50, description="Coordenada GPS de longitud")
    
    # Información de contacto
    phone: Optional[str] = Field(None, max_length=20, description="Teléfono principal de contacto")
    website: Optional[str] = Field(None, max_length=255, description="Sitio web oficial del proyecto")
    
    # Fechas
    start_date: Optional[date] = Field(None, description="Fecha de inicio del proyecto")
    delivery_date: Optional[date] = Field(None, description="Fecha de entrega del proyecto")
    delivery_end_date: Optional[date] = Field(None, description="Fecha de entrega final")
    launch_date: Optional[date] = Field(None, description="Fecha de lanzamiento del proyecto")
    
    # Precios y configuración
    price_from: Optional[Decimal] = Field(None, ge=0, description="Precio desde")
    price_to: Optional[Decimal] = Field(None, ge=0, description="Precio hasta")
    unique_price: Optional[Decimal] = Field(None, ge=0, description="Precio único")
    currency: str = Field(default="UF", description="Moneda")
    
    # Tipo de proyecto y entrega
    type: Optional[str] = Field(None, max_length=100, description="Tipo de proyecto")
    delivery_type: Optional[str] = Field(None, max_length=100, description="Tipo de entrega")
    
    # Estado y publicación
    state: str = Field(default="development", description="Estado del proyecto")
    is_active: bool = Field(True, description="Proyecto activo")
    is_published: bool = Field(False, description="Proyecto publicado")
    is_promo: bool = Field(False, description="Proyecto foco")
    is_hot: bool = Field(False, description="Proyecto destacado")
    
    # === INFORMACIÓN COMERCIAL OPCIONAL ===
    
    # Información de Postventa (3 campos)
    after_sales_email: Optional[str] = Field(None, max_length=255, description="Email del equipo de postventa")
    after_sales_executive: Optional[str] = Field(None, max_length=255, description="Ejecutivo responsable de postventa")
    after_sales_phone: Optional[str] = Field(None, max_length=20, description="Teléfono de postventa")
    
    # Información Financiera (7 campos)
    finances_insurance_company: Optional[str] = Field(None, max_length=255, description="Compañía aseguradora")
    finances_insurance_policy: Optional[str] = Field(None, max_length=100, description="Póliza de seguro")
    finances_insured_value: Optional[str] = Field(None, max_length=50, description="Valor asegurado total")
    finances_insured_value_util: Optional[str] = Field(None, max_length=50, description="Valor asegurado de utilidad")
    finances_benefit: Optional[str] = Field(None, max_length=50, description="Beneficio financiero")
    finances_annual_rate: Optional[Decimal] = Field(None, ge=0, description="Tasa anual (%)")
    finances_credit_rate: Optional[Decimal] = Field(None, ge=0, description="Tasa de crédito (%)")
    
    # Información Comercial Variable (12 campos)
    down_payment_bonus: Optional[Decimal] = Field(None, ge=0, description="Monto de bono pie")
    reservation: Optional[Decimal] = Field(None, ge=0, description="Monto de reserva")
    pre_approval: Optional[str] = Field(None, max_length=50, description="Categoría de pre-aprobación")
    installments: Optional[Decimal] = Field(None, ge=0, description="Monto de cuotas")
    balloon_payment: Optional[str] = Field(None, max_length=255, description="Información de cuotón")
    annual_capital_gain: Optional[Decimal] = Field(None, ge=0, description="Plusvalía anual estimada (%)")
    construction_capital_gain: Optional[Decimal] = Field(None, ge=0, description="Plusvalía durante construcción (%)")
    vacancy: Optional[Decimal] = Field(None, ge=0, description="Porcentaje de vacancia (%)")
    additional_information: Optional[str] = Field(None, description="Información adicional del proyecto")
    initial_payment: Optional[Decimal] = Field(None, ge=0, description="Abono inicial (%)")
    big_down_payment: Optional[Decimal] = Field(None, ge=0, description="Cuotón")
    notes_rent: Optional[Dict[str, Any]] = Field(None, description="Notas de arriendo como JSON estructurado")
    
    # Campos JSON Flexibles (4 campos)
    social_networks: Optional[Dict[str, Any]] = Field(None, description="URLs de redes sociales y tour virtual")
    payment_plan_conditions: Optional[Dict[str, Any]] = Field(None, description="Condiciones detalladas de pago")
    promotions_benefits: Optional[Dict[str, Any]] = Field(None, description="Promociones actuales y beneficios")
    frequently_asked_questions: Optional[Dict[str, Any]] = Field(None, description="Preguntas frecuentes")
    

    @validator('state')
    def validate_state(cls, v):
        if v not in PROJECT_STATES:
            raise ValueError(f'Estado de proyecto inválido. Opciones válidas: {", ".join(PROJECT_STATES)}')
        return v
    
    @validator('currency')
    def validate_currency(cls, v):
        if v not in CURRENCY_TYPES:
            raise ValueError(f'Moneda inválida. Opciones válidas: {", ".join(CURRENCY_TYPES)}')
        return v
    
    @validator('delivery_date')
    def validate_delivery_date_after_start(cls, v, values):
        if v is not None and 'start_date' in values and values['start_date'] is not None:
            if v <= values['start_date']:
                raise ValueError('La fecha de entrega debe ser posterior a la fecha de inicio')
        return v
    
    @validator('delivery_end_date')
    def validate_delivery_end_after_start(cls, v, values):
        if v is not None and 'delivery_date' in values and values['delivery_date'] is not None:
            if v <= values['delivery_date']:
                raise ValueError('La fecha de entrega final debe ser posterior a la fecha de entrega inicial')
        return v
    
    @validator('price_to')
    def validate_price_to_greater_than_from(cls, v, values):
        if v is not None and 'price_from' in values and values['price_from'] is not None:
            if v <= values['price_from']:
                raise ValueError('El precio máximo debe ser mayor al precio mínimo')
        return v


class ProjectUpdateRequest(BaseModel):
    """Schema para actualizar proyecto inmobiliario"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[Dict[str, Any]] = Field(None, description="Descripción del proyecto como JSON")
    executive: Optional[str] = Field(None, max_length=255)
    executive_email: Optional[str] = Field(None, max_length=255)
    
    # Ubicación
    city: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=100)
    address: Optional[str] = None
    street_number: Optional[str] = Field(None, max_length=20)
    commune: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, max_length=20)
    url_google_maps: Optional[str] = Field(None, max_length=500)
    latitude: Optional[str] = Field(None, max_length=50)
    longitude: Optional[str] = Field(None, max_length=50)
    
    # Contacto
    phone: Optional[str] = Field(None, max_length=20)
    website: Optional[str] = Field(None, max_length=255)
    
    # Fechas
    start_date: Optional[date] = None
    delivery_date: Optional[date] = None
    delivery_end_date: Optional[date] = None
    launch_date: Optional[date] = None
    
    # Precios y configuración
    price_from: Optional[Decimal] = Field(None, ge=0)
    price_to: Optional[Decimal] = Field(None, ge=0)
    unique_price: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    
    # Tipo de proyecto y entrega
    type: Optional[str] = Field(None, max_length=100)
    delivery_type: Optional[str] = Field(None, max_length=100)
    
    # Estado y publicación
    state: Optional[str] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None
    is_promo: Optional[bool] = None
    is_hot: Optional[bool] = None
    
    # === INFORMACIÓN COMERCIAL OPCIONAL ===
    
    # Información de Postventa
    after_sales_email: Optional[str] = Field(None, max_length=255)
    after_sales_executive: Optional[str] = Field(None, max_length=255)
    after_sales_phone: Optional[str] = Field(None, max_length=20)
    
    # Información Financiera
    finances_insurance_company: Optional[str] = Field(None, max_length=255)
    finances_insurance_policy: Optional[str] = Field(None, max_length=100)
    finances_insured_value: Optional[str] = Field(None, max_length=50)
    finances_insured_value_util: Optional[str] = Field(None, max_length=50)
    finances_benefit: Optional[str] = Field(None, max_length=50)
    finances_annual_rate: Optional[Decimal] = Field(None, ge=0)
    finances_credit_rate: Optional[Decimal] = Field(None, ge=0)
    
    # Información Comercial Variable
    down_payment_bonus: Optional[Decimal] = Field(None, ge=0)
    reservation: Optional[Decimal] = Field(None, ge=0)
    pre_approval: Optional[str] = Field(None, max_length=50)
    installments: Optional[Decimal] = Field(None, ge=0)
    balloon_payment: Optional[str] = Field(None, max_length=255)
    annual_capital_gain: Optional[Decimal] = Field(None, ge=0)
    construction_capital_gain: Optional[Decimal] = Field(None, ge=0)
    vacancy: Optional[Decimal] = Field(None, ge=0)
    additional_information: Optional[str] = None
    initial_payment: Optional[Decimal] = Field(None, ge=0)
    big_down_payment: Optional[Decimal] = Field(None, ge=0)
    notes_rent: Optional[Dict[str, Any]] = None
    
    # Campos JSON Flexibles
    social_networks: Optional[Dict[str, Any]] = None
    payment_plan_conditions: Optional[Dict[str, Any]] = None
    promotions_benefits: Optional[Dict[str, Any]] = None
    frequently_asked_questions: Optional[Dict[str, Any]] = None
    


class ProjectResponse(BaseResponse):
    """Schema de respuesta para proyecto inmobiliario"""
    id: int
    name: str
    description: Optional[Dict[str, Any]]
    company_id: int
    executive: Optional[str]
    executive_email: Optional[str]
    
    # Ubicación
    city: Optional[str]
    region: Optional[str]
    address: Optional[str]
    street_number: Optional[str]
    commune: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    url_google_maps: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    
    # Contacto
    phone: Optional[str]
    website: Optional[str]
    
    # Fechas
    start_date: Optional[date]
    delivery_date: Optional[date]
    delivery_end_date: Optional[date]
    launch_date: Optional[date]
    
    # Unidades y precios
    total_units: Optional[int]
    available_units: Optional[int]
    price_from: Optional[Decimal]
    price_to: Optional[Decimal]
    unique_price: Optional[Decimal]
    currency: str
    
    # Tipo de proyecto y entrega
    type: Optional[str]
    delivery_type: Optional[str]
    
    # Estado y fechas
    state: str
    is_active: bool
    is_published: bool
    is_promo: bool
    is_hot: bool
    created_at: datetime
    updated_at: datetime
    
    # === INFORMACIÓN COMERCIAL ===
    
    # Información de Postventa
    after_sales_email: Optional[str] = None
    after_sales_executive: Optional[str] = None
    after_sales_phone: Optional[str] = None
    
    # Información Financiera
    finances_insurance_company: Optional[str] = None
    finances_insurance_policy: Optional[str] = None
    finances_insured_value: Optional[str] = None
    finances_insured_value_util: Optional[str] = None
    finances_benefit: Optional[str] = None
    finances_annual_rate: Optional[Decimal] = None
    finances_credit_rate: Optional[Decimal] = None
    
    # Información Comercial Variable
    down_payment_bonus: Optional[Decimal] = None
    reservation: Optional[Decimal] = None
    pre_approval: Optional[str] = None
    installments: Optional[Decimal] = None
    balloon_payment: Optional[str] = None
    annual_capital_gain: Optional[Decimal] = None
    construction_capital_gain: Optional[Decimal] = None
    vacancy: Optional[Decimal] = None
    additional_information: Optional[str] = None
    initial_payment: Optional[Decimal] = None
    big_down_payment: Optional[Decimal] = None
    notes_rent: Optional[Dict[str, Any]] = None
    
    # Campos JSON Flexibles
    social_networks: Optional[Dict[str, Any]] = None
    payment_plan_conditions: Optional[Dict[str, Any]] = None
    promotions_benefits: Optional[Dict[str, Any]] = None
    frequently_asked_questions: Optional[Dict[str, Any]] = None


class ProjectListResponse(BaseModel):
    """Schema para lista paginada de proyectos"""
    projects: List[ProjectResponse]
    total: int
    page: int
    per_page: int
    total_pages: int


class ProjectStats(BaseModel):
    """Schema para estadísticas del proyecto"""
    total_units: int = Field(..., description="Total de unidades")
    available_units: int = Field(..., description="Unidades disponibles")
    reserved_units: int = Field(..., description="Unidades reservadas")
    sold_units: int = Field(..., description="Unidades vendidas")
    project_state: str = Field(..., description="Estado del proyecto")


class ProjectFilters(BaseModel):
    """Schema para filtros de búsqueda de proyectos"""
    company_id: Optional[int] = Field(None, ge=1)
    state: Optional[str] = None
    city: Optional[str] = Field(None, min_length=1)
    price_min: Optional[Decimal] = Field(None, ge=0)
    price_max: Optional[Decimal] = Field(None, ge=0)
    currency: Optional[str] = None
    is_active: Optional[bool] = None
    is_published: Optional[bool] = None


class ProjectStateUpdate(BaseModel):
    """Schema para actualización de estado del proyecto"""
    state: str = Field(..., description="Nuevo estado del proyecto")


# Nota: Los schemas comerciales separados han sido eliminados
# Toda la información comercial ahora se maneja directamente en los schemas de Project 


# Schemas para Project Details Endpoint
class CompanyInfo(BaseModel):
    id: int
    name: str
    legal_name: Optional[str] = None
    rut: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True


class ProjectStockInfo(BaseModel):
    id: int
    unit_number: str
    unit_type: str
    description: Optional[str] = None
    bedrooms: int
    bathrooms: int
    orientation: Optional[str] = None
    total_area: Optional[Decimal] = None
    floor: Optional[int] = None
    building: Optional[str] = None
    has_parking: bool
    has_storage: bool
    storages: Optional[str] = None
    parkings: Optional[str] = None
    surface_internal: Optional[Decimal] = None
    surface_terrace: Optional[Decimal] = None
    currency: str
    value_base: Optional[Decimal] = None
    value_uf: Optional[Decimal] = None
    value_parking: Optional[Decimal] = None
    value_storage: Optional[Decimal] = None
    status: str

    class Config:
        from_attributes = True


class ProjectImageInfo(BaseModel):
    id: int
    filename: str
    url: str
    alt_text: Optional[str] = None
    image_type: str
    is_featured: bool
    display_order: int

    class Config:
        from_attributes = True


class ProjectDocumentInfo(BaseModel):
    id: int
    filename: str
    url: str
    document_type: str
    is_active: bool

    class Config:
        from_attributes = True


class ProjectCommercialInfo(BaseModel):
    id: int
    after_sales_email: Optional[str] = None
    after_sales_executive: Optional[str] = None
    after_sales_phone: Optional[str] = None
    finances_insurance_company: Optional[str] = None
    finances_insurance_policy: Optional[str] = None
    finances_insured_value: Optional[str] = None
    finances_insured_value_util: Optional[str] = None
    finances_benefit: Optional[str] = None
    finances_annual_rate: Optional[Decimal] = None
    finances_credit_rate: Optional[Decimal] = None
    down_payment_bonus: Optional[Decimal] = None
    reservation: Optional[Decimal] = None
    pre_approval: Optional[str] = None
    installments: Optional[Decimal] = None
    balloon_payment: Optional[str] = None
    annual_capital_gain: Optional[Decimal] = None
    construction_capital_gain: Optional[Decimal] = None
    vacancy: Optional[Decimal] = None
    additional_information: Optional[str] = None
    initial_payment: Optional[Decimal] = None
    big_down_payment: Optional[Decimal] = None
    notes_rent: Optional[Dict[str, Any]] = None
    social_networks: Optional[Dict[str, Any]] = None
    payment_plan_conditions: Optional[Dict[str, Any]] = None
    promotions_benefits: Optional[Dict[str, Any]] = None
    frequently_asked_questions: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True


class ProjectInfo(BaseModel):
    id: int
    name: str
    description: Optional[Dict[str, Any]]
    company_id: int
    executive: Optional[str]
    executive_email: Optional[str]
    city: Optional[str]
    region: Optional[str]
    address: Optional[str]
    street_number: Optional[str]
    commune: Optional[str]
    country: Optional[str]
    postal_code: Optional[str]
    url_google_maps: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    phone: Optional[str]
    website: Optional[str]
    start_date: Optional[date]
    delivery_date: Optional[date]
    delivery_end_date: Optional[date]
    launch_date: Optional[date]
    total_units: Optional[int]
    available_units: Optional[int]
    price_from: Optional[Decimal]
    price_to: Optional[Decimal]
    unique_price: Optional[Decimal]
    currency: str
    type: Optional[str]
    delivery_type: Optional[str]
    state: str
    is_active: bool
    is_published: bool
    is_promo: bool
    is_hot: bool
    created_at: datetime
    updated_at: datetime
    commercial: Optional[ProjectCommercialInfo] = None
    
    class Config:
        from_attributes = True


class ProjectDetailsResponse(BaseModel):
    project: ProjectInfo
    company: CompanyInfo
    stock: List[ProjectStockInfo]
    images: List[ProjectImageInfo]
    documents: List[ProjectDocumentInfo]

    class Config:
        from_attributes = True