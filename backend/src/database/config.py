"""
Configuración de base de datos
"""

import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Configuración de la base de datos"""
    
    HOST: str = os.environ.get("DB_HOST", "localhost")
    PORT: int = int(os.environ.get("DB_PORT", "3306"))
    NAME: str = os.environ.get("DB_NAME", "real_estate_app")
    USER: str = os.environ.get("DB_USER", "root")
    PASSWORD: str = os.environ.get("DB_PASSWORD", "")
    
    API_KEY: str = os.environ.get("API_KEY", "test-api-key-development")
    
    @property
    def database_url(self) -> str:
        """URL de conexión MySQL para SQLAlchemy"""
        return f"mysql+aiomysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"


db_config = DatabaseConfig() 