"""
Modelos SQLAlchemy para API de Proyectos Inmobiliarios
Todos los modelos independientes sin herencia
"""

from sqlalchemy import Column, String, Text, Boolean, Integer, BigInteger, Numeric, ForeignKey, Date, Index, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database.base import Base


class RbacUser(Base):
    """Modelo para usuarios RBAC - Tabla existente"""
    
    __tablename__ = "rbac_users"
    
    # Mapear exactamente como está en la tabla
    id = Column('iduser', BigInteger, primary_key=True, autoincrement=True, index=True)
    nomcompleto = Column(String(255), nullable=True)
    nuser = Column(String(255), nullable=True, unique=True)
    telefono = Column(String(50), nullable=True)
    token = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.current_timestamp(), nullable=True)
    update_at = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    staff = Column(Integer, nullable=False)
    estado = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<RbacUser(id={self.id}, nuser='{self.nuser}')>"


class RealEstateCompany(Base):
    """Modelo para inmobiliarias"""
    
    __tablename__ = "real_estate_companies"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Información básica
    name = Column(String(255), nullable=False)
    legal_name = Column(String(255), nullable=True)
    rut = Column(String(12), nullable=True, unique=True)
    
    # Contacto
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    website = Column(String(255), nullable=True)
    
    # Dirección
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Relaciones
    projects = relationship("Project", back_populates="company", cascade="all, delete-orphan")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_company_name", "name"),
        Index("idx_company_rut", "rut"),
        Index("idx_company_active", "is_active"),
        Index("idx_company_city", "city"),
        Index("idx_company_created_by", "created_by"),
        Index("idx_company_updated_by", "updated_by"),
    )
    
    def __repr__(self):
        return f"<RealEstateCompany(id={self.id}, name='{self.name}')>"


class Project(Base):
    """Modelo para proyectos inmobiliarios"""
    
    __tablename__ = "projects"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Información básica
    company_id = Column(BigInteger, ForeignKey("real_estate_companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(JSON, nullable=True)  # MODIFICADO: Text → JSON para contenido estructurado
    
    # Información de gestión
    executive = Column(String(255), nullable=True)  # Ejecutivo responsable del proyecto
    executive_email = Column(String(255), nullable=True)  # Email del ejecutivo responsable
    
    # Ubicación
    city = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    street_number = Column(String(20), nullable=True)  # Número de calle/dirección
    commune = Column(String(100), nullable=True)  # Comuna del proyecto
    country = Column(String(100), nullable=True)  # País donde se ubica el proyecto
    postal_code = Column(String(20), nullable=True)  # Código postal
    url_google_maps = Column(String(500), nullable=True)  # URL de ubicación en Google Maps
    latitude = Column(String(50), nullable=True)  # Coordenada GPS de latitud
    longitude = Column(String(50), nullable=True)  # Coordenada GPS de longitud
    
    # Información de contacto
    phone = Column(String(20), nullable=True)  # Teléfono principal de contacto
    website = Column(String(255), nullable=True)  # Sitio web oficial del proyecto
    
    # Precios
    price_from = Column(Numeric(15, 2), nullable=True)
    price_to = Column(Numeric(15, 2), nullable=True)
    unique_price = Column(Numeric(15, 2), nullable=True)  # Precio único
    currency = Column(String(10), default="CLP", nullable=False)
    
    # Unidades
    total_units = Column(Integer, nullable=True)
    available_units = Column(Integer, nullable=True)
    
    # Tipo y Estado
    type = Column(String(100), nullable=True)  # Tipo de proyecto
    delivery_type = Column(String(100), nullable=True)  # Tipo de entrega
    state = Column(String(50), default="development", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    is_promo = Column(Boolean, default=False, nullable=False)  # Proyecto foco
    is_hot = Column(Boolean, default=False, nullable=False)  # Proyecto destacado
    
    # Fechas
    start_date = Column(Date, nullable=True)
    delivery_date = Column(Date, nullable=True)
    delivery_end_date = Column(Date, nullable=True)  # Fecha de entrega final
    launch_date = Column(Date, nullable=True)  # Fecha de lanzamiento del proyecto
    
    # Relaciones
    company = relationship("RealEstateCompany", back_populates="projects")
    commercial = relationship("ProjectCommercial", back_populates="project", uselist=False, cascade="all, delete-orphan")
    stock_units = relationship("ProjectStock", back_populates="project", cascade="all, delete-orphan")
    images = relationship("ProjectImage", back_populates="project", cascade="all, delete-orphan")
    documents = relationship("ProjectDocument", back_populates="project", cascade="all, delete-orphan")
    legal_users = relationship("LegalUser", back_populates="project", cascade="all, delete-orphan")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_project_name", "name"),
        Index("idx_project_city", "city"),
        Index("idx_project_commune", "commune"),
        Index("idx_project_state", "state"),
        Index("idx_project_active", "is_active"),
        Index("idx_project_company", "company_id"),
        Index("idx_project_created_by", "created_by"),
        Index("idx_project_updated_by", "updated_by"),
        # Índices para campos nuevos
        Index("idx_project_executive", "executive"),
        Index("idx_project_executive_email", "executive_email"),
        Index("idx_project_street_number", "street_number"),
        Index("idx_project_country", "country"),
        Index("idx_project_launch_date", "launch_date"),
        Index("idx_project_delivery_end_date", "delivery_end_date"),
        Index("idx_project_type", "type"),
        Index("idx_project_delivery_type", "delivery_type"),
        Index("idx_project_unique_price", "unique_price"),
        Index("idx_project_is_promo", "is_promo"),
        Index("idx_project_is_hot", "is_hot"),
    )
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class ProjectStock(Base):
    """Modelo para stock de proyectos"""
    
    __tablename__ = "project_stock"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Información básica
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False)
    unit_number = Column(String(50), nullable=False)
    unit_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    
    # Características
    bedrooms = Column(Integer, default=0, nullable=False)
    bathrooms = Column(Integer, default=0, nullable=False)
    orientation = Column(String(50), nullable=True)
    total_area = Column(Numeric(8, 2), nullable=True)
    
    # Ubicación
    floor = Column(Integer, nullable=True)
    building = Column(String(50), nullable=True)
    
    # Estacionamientos y bodegas
    parkings = Column(String(50), nullable=True)  # Información de estacionamientos
    storages = Column(String(50), nullable=True)  # Información de bodegas
    has_parking = Column(Boolean, default=False, nullable=False)
    has_storage = Column(Boolean, default=False, nullable=False)
    
    # Superficies (todas en m²)
    surface_internal = Column(Numeric(8, 2), nullable=True)
    surface_terrace = Column(Numeric(8, 2), nullable=True)
    surface_garden = Column(Numeric(8, 2), nullable=True)
    surface_pantry = Column(Numeric(8, 2), nullable=True)
    surface_multiuse_assignable = Column(Numeric(8, 2), nullable=True)
    surface_util = Column(Numeric(8, 2), nullable=True)
    surface_terrain = Column(Numeric(8, 2), nullable=True)
    surface_others = Column(Numeric(8, 2), nullable=True)
    
    # Precios y valores
    currency = Column(String(10), default="CLP", nullable=False)
    value_base = Column(Numeric(15, 2), nullable=True)
    value_uf = Column(Numeric(10, 2), nullable=True)  # Mantener campo existente
    value_list = Column(Numeric(15, 2), nullable=True)
    value_discount = Column(Numeric(15, 2), nullable=True)
    value_enabled = Column(Numeric(15, 2), nullable=True)
    value_promotion = Column(Numeric(15, 2), nullable=True)
    value_bonus = Column(Numeric(15, 2), nullable=True)
    value_parking = Column(Numeric(15, 2), nullable=True)  # Valor del estacionamiento
    value_storage = Column(Numeric(15, 2), nullable=True)  # Valor de la bodega
    
    # Estado
    status = Column(String(50), default="available", nullable=False)
    
    # Relaciones
    project = relationship("Project", back_populates="stock_units")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_stock_project", "project_id"),
        Index("idx_stock_status", "status"),
        Index("idx_stock_bedrooms", "bedrooms"),
        Index("idx_stock_bathrooms", "bathrooms"),
        Index("idx_stock_orientation", "orientation"),
        Index("idx_stock_currency", "currency"),
        Index("idx_stock_price", "value_base"),
        Index("idx_stock_price_list", "value_list"),
        Index("idx_stock_floor", "floor"),
        Index("idx_stock_building", "building"),
        Index("idx_stock_unique_unit", "project_id", "unit_number", unique=True),
        Index("idx_stock_created_by", "created_by"),
        Index("idx_stock_updated_by", "updated_by"),
        # Índices para campos nuevos
        Index("idx_stock_value_parking", "value_parking"),
        Index("idx_stock_value_storage", "value_storage"),
    )
    
    def __repr__(self):
        return f"<ProjectStock(id={self.id}, unit='{self.unit_number}')>"


class LegalUser(Base):
    """Modelo para representantes legales de proyectos"""
    
    __tablename__ = "legal_users"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Información básica
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    rut = Column(String(12), nullable=True)
    
    # Contacto
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Información profesional
    position = Column(String(100), nullable=True)
    company = Column(String(255), nullable=True)
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False)
    is_primary = Column(Boolean, default=False, nullable=False)
    
    # Relaciones
    project = relationship("Project", back_populates="legal_users")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_legal_user_project", "project_id"),
        Index("idx_legal_user_active", "is_active"),
        Index("idx_legal_user_primary", "is_primary"),
        Index("idx_legal_user_name", "first_name", "last_name"),
        Index("idx_legal_user_created_by", "created_by"),
        Index("idx_legal_user_updated_by", "updated_by"),
    )
    
    def __repr__(self):
        return f"<LegalUser(id={self.id}, name='{self.first_name} {self.last_name}')>"


class ProjectImage(Base):
    """Modelo para imágenes de proyectos"""
    
    __tablename__ = "project_images"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Información básica
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    
    # Descripción
    alt_text = Column(String(255), nullable=True)
    image_type = Column(String(50), default="general", nullable=False)
    
    # Configuración
    is_featured = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    display_order = Column(Integer, default=0, nullable=False)
    
    # Relaciones
    project = relationship("Project", back_populates="images")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_project_image_project", "project_id"),
        Index("idx_project_image_type", "image_type"),
        Index("idx_project_image_featured", "is_featured"),
        Index("idx_project_image_order", "project_id", "display_order"),
        Index("idx_project_image_created_by", "created_by"),
        Index("idx_project_image_updated_by", "updated_by"),
    )
    
    def __repr__(self):
        return f"<ProjectImage(id={self.id}, filename='{self.filename}')>" 


class ProjectDocument(Base):
    """Modelo para documentos de proyectos"""
    
    __tablename__ = "project_documents"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Información básica
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    url = Column(String(500), nullable=False)
    
    # Tipo de documento
    document_type = Column(String(50), default="general", nullable=False)
    
    # Estado
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Relaciones
    project = relationship("Project", back_populates="documents")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_project_document_project", "project_id"),
        Index("idx_project_document_type", "document_type"),
        Index("idx_project_document_active", "is_active"),
        Index("idx_project_document_created_by", "created_by"),
        Index("idx_project_document_updated_by", "updated_by"),
    )
    
    def __repr__(self):
        return f"<ProjectDocument(id={self.id}, filename='{self.filename}')>" 


class ProjectCommercial(Base):
    """Modelo para información comercial de proyectos"""
    
    __tablename__ = "project_commercial"
    
    # Campos estándar
    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Auditoría
    created_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    updated_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    deleted_by = Column(BigInteger, ForeignKey("rbac_users.iduser"), nullable=True)
    
    # Relación con proyecto (1:1)
    project_id = Column(BigInteger, ForeignKey("projects.id"), nullable=False, unique=True)
    
    # === CAMPOS COMERCIALES ===
    
    # Información de Postventa (3 campos)
    after_sales_email = Column(String(255), nullable=True)  # Email del equipo de postventa
    after_sales_executive = Column(String(255), nullable=True)  # Ejecutivo responsable de postventa
    after_sales_phone = Column(String(20), nullable=True)  # Teléfono de postventa
    
    # Información Financiera (7 campos)
    finances_insurance_company = Column(String(255), nullable=True)  # Compañía aseguradora
    finances_insurance_policy = Column(String(100), nullable=True)  # Póliza de seguro
    finances_insured_value = Column(String(50), nullable=True)  # Valor asegurado total
    finances_insured_value_util = Column(String(50), nullable=True)  # Valor asegurado de utilidad
    finances_benefit = Column(String(50), nullable=True)  # Beneficio financiero
    finances_annual_rate = Column(Numeric(5, 2), nullable=True)  # Tasa anual (%)
    finances_credit_rate = Column(Numeric(5, 2), nullable=True)  # Tasa de crédito (%)
    
    # Información Comercial Variable (10 campos)
    down_payment_bonus = Column(Numeric(15, 2), nullable=True)  # Monto de bono pie
    reservation = Column(Numeric(15, 2), nullable=True)  # Monto de reserva
    pre_approval = Column(String(50), nullable=True)  # categoria de pre-aprobacion
    installments = Column(Numeric(15, 2), nullable=True)  # Monto de cuotas
    balloon_payment = Column(String(255), nullable=True)  # Información de cuotón
    annual_capital_gain = Column(Numeric(5, 2), nullable=True)  # Plusvalía anual estimada (%)
    construction_capital_gain = Column(Numeric(5, 2), nullable=True)  # Plusvalía durante construcción (%)
    vacancy = Column(Numeric(5, 2), nullable=True)  # Porcentaje de vacancia (%)
    additional_information = Column(Text, nullable=True)  # Información adicional del proyecto
    initial_payment = Column(Numeric(5, 2), nullable=True)  # Abono inicial (%)
    big_down_payment = Column(Numeric(15, 2), nullable=True)  # Cuotón
    notes_rent = Column(JSON, nullable=True)  # Notas de arriendo como JSON estructurado
    
    # Campos JSON Flexibles (4 campos)
    social_networks = Column(JSON, nullable=True)  # URLs de redes sociales y tour virtual
    payment_plan_conditions = Column(JSON, nullable=True)  # Condiciones detalladas de pago
    promotions_benefits = Column(JSON, nullable=True)  # Promociones actuales y beneficios
    frequently_asked_questions = Column(JSON, nullable=True)  # Preguntas frecuentes
    
    # Relaciones
    project = relationship("Project", back_populates="commercial")
    created_by_user = relationship("RbacUser", foreign_keys=[created_by])
    updated_by_user = relationship("RbacUser", foreign_keys=[updated_by])
    deleted_by_user = relationship("RbacUser", foreign_keys=[deleted_by])
    
    # Índices
    __table_args__ = (
        Index("idx_project_commercial_project", "project_id"),
        Index("idx_project_commercial_after_sales", "after_sales_executive"),
        Index("idx_project_commercial_initial_payment", "initial_payment"),
        Index("idx_project_commercial_big_down_payment", "big_down_payment"),
        Index("idx_project_commercial_created_by", "created_by"),
        Index("idx_project_commercial_updated_by", "updated_by"),
        # Índices para campos numéricos nuevos
        Index("idx_project_commercial_finances_annual_rate", "finances_annual_rate"),
        Index("idx_project_commercial_finances_credit_rate", "finances_credit_rate"),
        Index("idx_project_commercial_down_payment_bonus", "down_payment_bonus"),
        Index("idx_project_commercial_reservation", "reservation"),
        Index("idx_project_commercial_pre_approval", "pre_approval"),
        Index("idx_project_commercial_installments", "installments"),
        Index("idx_project_commercial_annual_capital_gain", "annual_capital_gain"),
        Index("idx_project_commercial_construction_capital_gain", "construction_capital_gain"),
        Index("idx_project_commercial_vacancy", "vacancy"),
    )
    
    def __repr__(self):
        return f"<ProjectCommercial(id={self.id}, project_id={self.project_id})>"