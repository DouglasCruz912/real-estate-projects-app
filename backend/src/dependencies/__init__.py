"""
Dependencias de FastAPI
"""

from .db_dependencies import DatabaseDep
from .auth_dependencies import RequireAPIKey

__all__ = [
    "DatabaseDep",
    "RequireAPIKey"
]
