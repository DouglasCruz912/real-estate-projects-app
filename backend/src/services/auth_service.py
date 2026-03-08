"""
Servicio de autenticación: hashing de passwords y JWT
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import jwt, JWTError

from ..database.config import db_config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=db_config.JWT_EXPIRATION_MINUTES)
    )
    to_encode["exp"] = expire
    return jwt.encode(to_encode, db_config.JWT_SECRET_KEY, algorithm=db_config.JWT_ALGORITHM)


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, db_config.JWT_SECRET_KEY, algorithms=[db_config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
