"""
Excepciones personalizadas para la API de Proyectos
"""

from fastapi import HTTPException, status
from typing import Optional, Dict, Any


class APIException(HTTPException):
    """Excepción base personalizada para la API"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "API_ERROR",
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


class AuthenticationError(APIException):
    """Error de autenticación"""
    
    def __init__(self, detail: str = "API key requerida"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="AUTHENTICATION_ERROR",
            headers={"X-Error-Code": "INVALID_API_KEY"}
        )


class AuthorizationError(APIException):
    """Error de autorización"""
    
    def __init__(self, detail: str = "API key inválida"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="AUTHORIZATION_ERROR",
            headers={"X-Error-Code": "FORBIDDEN"}
        )


class ValidationError(APIException):
    """Error de validación de datos"""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        # Usar solo el mensaje pasado, sin agregar texto adicional
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )


class NotFoundError(APIException):
    """Error de recurso no encontrado"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND_ERROR"
        )


class ConflictError(APIException):
    """Error de conflicto"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT_ERROR"
        )


class DatabaseError(APIException):
    """Error de base de datos"""
    
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code="DATABASE_ERROR"
        )


class CacheError(APIException):
    """Error de cache"""
    
    def __init__(self, detail: str = "Cache operation failed"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            error_code="CACHE_ERROR"
        )


class RateLimitError(APIException):
    """Error de límite de velocidad"""
    
    def __init__(self, detail: str = "Rate limit exceeded"):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=detail,
            error_code="RATE_LIMIT_ERROR",
            headers={"Retry-After": "60"}
        )


class BusinessLogicError(APIException):
    """Error de lógica de negocio"""
    
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BUSINESS_LOGIC_ERROR"
        )


# Excepciones específicas del dominio
class ProjectNotFoundError(NotFoundError):
    """Proyecto no encontrado"""
    
    def __init__(self, project_id: Any):
        super().__init__(f"Proyecto con ID {project_id} no encontrado")


class CompanyNotFoundError(NotFoundError):
    """Inmobiliaria no encontrada"""
    
    def __init__(self, company_id: Any):
        super().__init__(f"Inmobiliaria con ID {company_id} no encontrada")


class StockUnitNotFoundError(NotFoundError):
    """Unidad de stock no encontrada"""
    
    def __init__(self, stock_id: Any):
        super().__init__(f"Unidad de stock con ID {stock_id} no encontrada")


class DuplicateProjectError(ConflictError):
    """Proyecto duplicado"""
    
    def __init__(self, message: str):
        super().__init__(message)


class DuplicateCompanyError(ConflictError):
    """Inmobiliaria duplicada"""
    
    def __init__(self, message: str):
        super().__init__(message)


class InvalidStockStatusError(BusinessLogicError):
    """Estado de stock inválido"""
    
    def __init__(self, message: str):
        super().__init__(message)


class StockNotAvailableError(BusinessLogicError):
    """Stock no disponible"""
    
    def __init__(self, message: str):
        super().__init__(message)


# Nota: Las excepciones específicas se manejan directamente sin funciones intermedias
# Cada raise debe usar la excepción apropiada según el contexto 