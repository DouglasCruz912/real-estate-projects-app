"""
Schemas de Pydantic para la API de Proyectos
Organizados por entidad para mejor mantenimiento
"""

# Base schemas
from .base import BaseResponse, PaginatedResponse, MessageResponse

# Company schemas
from .companies import (
    CompanyCreate,
    CompanyUpdate,
    CompanyResponse
)

# Project schemas
from .projects import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectResponse,
    ProjectListResponse
)

# Stock schemas
from .stock import (
    StockCreateRequest,
    StockUpdateRequest,
    StockResponse,
    StockListResponse
)

# User schemas
from .users import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInfo
)

__all__ = [
    # Base
    "BaseResponse",
    "PaginatedResponse", 
    "MessageResponse",
    
    # Companies
    "CompanyCreate",
    "CompanyUpdate",
    "CompanyResponse",
    
    # Projects
    "ProjectCreateRequest",
    "ProjectUpdateRequest",
    "ProjectResponse",
    "ProjectListResponse",
    
    # Stock
    "StockCreateRequest",
    "StockUpdateRequest",
    "StockResponse",
    "StockListResponse",
    
    # Users
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInfo"
] 