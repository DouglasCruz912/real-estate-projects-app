"""
Configuración simple de base de datos
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()


class DatabaseConfig:
    """Configuración simple y directa de la base de datos"""
    
    # === DATABASE ===
    HOST: str = os.environ.get("DB_HOST", "localhost")
    PORT: int = int(os.environ.get("DB_PORT", "3306"))
    NAME: str = os.environ.get("DB_NAME", "propital_projects")
    USER: str = os.environ.get("DB_USER", "root")
    PASSWORD: str = os.environ.get("DB_PASSWORD", "")  # Contraseña vacía por defecto
    
    # === REDIS (OPCIONAL) ===
    REDIS_HOST: str = os.environ.get("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_PASSWORD: Optional[str] = os.environ.get("REDIS_PASSWORD")
    
    # === API ===
    API_KEY: str = os.environ.get("API_KEY", "test-api-key-development")
    
    @property
    def database_url(self) -> str:
        """URL de conexión MySQL para SQLAlchemy"""
        return f"mysql+aiomysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"
    
    @property
    def redis_url(self) -> str:
        """URL de conexión Redis"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/0"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/0"


# Instancia global
db_config = DatabaseConfig() 