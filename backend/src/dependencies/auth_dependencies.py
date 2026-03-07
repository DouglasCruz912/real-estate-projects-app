"""
Validación simple de API key - Solo header X-API-Key
"""

from fastapi import HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from typing import Optional
from ..database.config import db_config

# Esquema de seguridad para FastAPI
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def validate_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """
    Validación simple de API key - Solo header X-API-Key
    """
    
    # Validar que se proporcione API key
    if not api_key:
        raise HTTPException(
            status_code=401, 
            detail="API key requerida en header 'X-API-Key'"
        )
    
    # Validar que sea correcta
    if api_key != db_config.API_KEY:
        raise HTTPException(
            status_code=403,
            detail="API key inválida"
        )
    
    return True


# Dependencia simple para endpoints que muestra candado en Swagger
RequireAPIKey = Security(validate_api_key) 