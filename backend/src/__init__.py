"""
API de Proyectos Inmobiliarios
Módulo principal con arquitectura híbrida optimizada
"""

__version__ = "1.0.0"
__author__ = "Equipo Propitácora"
__description__ = "API REST para gestión de proyectos inmobiliarios y stock"

# Imports principales
from . import database
from . import models
from . import schemas
from . import services
from . import routers
from . import utils
from . import middleware
from . import dependencies

__all__ = [
    "database",
    "models",
    "schemas", 
    "services",
    "routers",
    "utils",
    "middleware",
    "dependencies"
] 