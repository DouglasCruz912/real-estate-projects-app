"""
Dependencias de FastAPI simplificadas
"""

from .db_dependencies import DatabaseDep, RedisDep
from .auth_dependencies import RequireAPIKey

__all__ = [
    "DatabaseDep",
    "RedisDep", 
    "RequireAPIKey"
] 