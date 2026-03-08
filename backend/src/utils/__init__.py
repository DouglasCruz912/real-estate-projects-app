"""
Módulo de utilidades
"""

from .exceptions import *
from .validation import *
from .helpers import *
from .constants import *

__all__ = [
    # Exceptions
    "APIException",
    "AuthenticationError",
    "AuthorizationError", 
    "ValidationError",
    "NotFoundError",
    "ConflictError",
    "DatabaseError",
    "CacheError",
    "RateLimitError",
    "BusinessLogicError",
    "ProjectNotFoundError",
    "CompanyNotFoundError",
    "StockUnitNotFoundError",
    "DuplicateProjectError",
    "DuplicateCompanyError",
    "InvalidStockStatusError",
    "StockNotAvailableError",
    
    # Validation
    "validate_tax_id",
    "validate_email", 
    "validate_phone",
    "validate_price",
    "validate_area",
    "validate_coordinates",
    "normalize_phone",
    "validate_project_status",
    "validate_stock_status",
    "validate_project_type",
    "validate_unit_type",
    
    # Helpers
    "generate_request_id",
    "generate_cache_key",
    "format_price",
    "format_area",
    "format_datetime",
    "parse_datetime",
    "clean_dict",
    "merge_dicts",
    "paginate_results",
    "calculate_percentage",
    "safe_divide",
    "format_file_size",
    "truncate_text",
    "generate_slug",
    "extract_numbers",
    "is_valid_uuid",
    "deep_get",
    "deep_set",
    "batch_process",
    "retry_on_exception",
    "get_client_ip",
    "mask_sensitive_data",
    
    # Constants
    "PROJECT_STATUS",
    "STOCK_STATUS",
    "PROJECT_TYPES",
    "UNIT_TYPES",
    "IMAGE_TYPES",
    "PAGINATION",
    "CACHE_CONFIG",
    "VALIDATION_LIMITS",
    "ERROR_MESSAGES",
    "API_CONFIG",
    "RESPONSE_HEADERS"
]
