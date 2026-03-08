"""
Dependencias de autenticación: API Key y JWT
"""

from fastapi import HTTPException, Depends, Security
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.config import db_config
from ..services.auth_service import decode_access_token
from ..services import user_service
from .db_dependencies import get_db

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
bearer_scheme = HTTPBearer(auto_error=False)


async def validate_api_key(api_key: Optional[str] = Security(api_key_header)) -> bool:
    """Validación simple de API key - Solo header X-API-Key"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API key requerida en header 'X-API-Key'")
    if api_key != db_config.API_KEY:
        raise HTTPException(status_code=403, detail="API key inválida")
    return True


RequireAPIKey = Security(validate_api_key)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Extraer y validar usuario desde JWT Bearer token"""
    if not credentials:
        raise HTTPException(status_code=401, detail="Token de autenticación requerido")
    
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    
    user_id: Optional[int] = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Token inválido")
    
    user = await user_service.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado o inactivo")
    
    return user


RequireAuth = Depends(get_current_user)


async def require_admin(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(bearer_scheme),
    db: AsyncSession = Depends(get_db),
):
    """Requiere JWT + rol admin"""
    user = await get_current_user(credentials, db)
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return user


RequireAdmin = Depends(require_admin)
