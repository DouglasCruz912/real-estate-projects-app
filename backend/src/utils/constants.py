"""
Constantes de la API de Proyectos
"""

# Estados de proyecto
PROJECT_STATUS = {
    'PLANNING': 'planning',#Planificación
    'CONSTRUCTION': 'construction', #En construcción
    'PRE_SALE': 'pre_sale',#Pre-venta
    'SALE': 'sale',#En venta
    'DELIVERED': 'delivered',#Entregado
    'COMPLETED': 'completed',#Completado
    'CANCELLED': 'cancelled'#Cancelado
}

# Estados de stock
STOCK_STATUS = {
    'AVAILABLE': 'available',#Disponible
    'RESERVED': 'reserved',#Reservado
    'SOLD': 'sold',#Vendido
    'BLOCKED': 'blocked'#Bloqueado
}

# Tipos de proyecto
PROJECT_TYPES = {
    'APARTMENT': 'apartment',#Departamento
    'HOUSE': 'house',#Casa
    'OFFICE': 'office',#Oficina
    'COMMERCIAL': 'commercial',#Local comercial
    'INDUSTRIAL': 'industrial',#Industrial
    'LAND': 'land',#Terreno
    'MIXED': 'mixed'#Mixto
}

# Tipos de unidad
UNIT_TYPES = {
    'APARTMENT': 'apartment',#Departamento
    'HOUSE': 'house',#Casa
    'OFFICE': 'office',#Oficina
    'STORE': 'store',#Local comercial
    'WAREHOUSE': 'warehouse',#Bodega
    'PARKING': 'parking',#Estacionamiento
    'STORAGE': 'storage',#Bodega de almacenamiento
    'TOWNHOUSE': 'townhouse',#Casa adosada
    'COMMERCIAL': 'commercial',#Local comercial
    'LAND': 'land'#Terreno
}

# Tipos de imagen
IMAGE_TYPES = {
    'GENERAL': 'general',#General
    'EXTERIOR': 'exterior',#Exterior
    'INTERIOR': 'interior',#Interior
    'AMENITIES': 'amenities',#Amenidades
    'FLOOR_PLAN': 'floor_plan',#Plano de piso
    'LOCATION': 'location'#Ubicación
}


# Límites de paginación
PAGINATION = {
    'DEFAULT_LIMIT': 100,
    'MAX_LIMIT': 500,
    'MIN_LIMIT': 1
}

# Configuración de cache
CACHE_CONFIG = {
    'DEFAULT_TTL': 300,  # 5 minutos
    'PROJECT_DETAILS_TTL': 3600,  # 1 hora
    'SEARCH_TTL': 900,  # 15 minutos
    'STOCK_SUMMARY_TTL': 1800  # 30 minutos
}

# Monedas soportadas
CURRENCY_TYPES = ['USD', 'EUR', 'CLP', 'UF', 'MXN', 'COP', 'ARS', 'PEN', 'BRL']

# Estados de proyecto actualizados
PROJECT_STATES = [
    'planning',      # Planificación
    'development',   # En desarrollo  
    'pre_sale',      # Pre-venta
    'construction',  # En construcción
    'sale',         # En venta
    'delivered',    # Entregado
    'completed',    # Completado
    'cancelled'     # Cancelado
]

# Estados de stock
STOCK_STATES = [
    'available',    # Disponible
    'reserved',     # Reservado
    'sold',        # Vendido
    'blocked'      # Bloqueado
]

# Tipos de propiedad
PROPERTY_TYPES = [
    'apartment',    # Departamento
    'house',       # Casa
    'townhouse',   # Casa adosada
    'office',      # Oficina
    'commercial',  # Local comercial
    'warehouse',   # Bodega
    'parking',     # Estacionamiento
    'storage',     # Bodega de almacenamiento
    'land'         # Terreno
]

# Configuración de validación por moneda
VALIDATION_LIMITS = {
    'UF': {
        'MIN_PRICE': 500,        # 500 UF mínimo (~$17M CLP)
        'MAX_PRICE': 100000,     # 100,000 UF máximo (~$3.4B CLP)
        'TYPICAL_MIN': 1000,     # 1,000 UF típico para departamentos
        'TYPICAL_MAX': 50000     # 50,000 UF típico para casas de lujo
    },
    'CLP': {
        'MIN_PRICE': 500000,     # $500K CLP mínimo
        'MAX_PRICE': 10000000000, # $10B CLP máximo
        'TYPICAL_MIN': 20000000,  # $20M CLP típico
        'TYPICAL_MAX': 1000000000 # $1B CLP típico
    },
    'USD': {
        'MIN_PRICE': 10000,      # $10K USD mínimo
        'MAX_PRICE': 5000000,    # $5M USD máximo
        'TYPICAL_MIN': 50000,    # $50K USD típico
        'TYPICAL_MAX': 1000000   # $1M USD típico
    },
    'AREA': {
        'MIN_AREA': 1,           # 1 m² mínimo
        'MAX_AREA': 100000,      # 100,000 m² máximo
        'TYPICAL_MIN': 20,       # 20 m² típico para departamentos pequeños
        'TYPICAL_MAX': 5000      # 5,000 m² típico para casas grandes
    },
    'ROOMS': {
        'MIN_BEDROOMS': 0,
        'MAX_BEDROOMS': 20,
        'MIN_BATHROOMS': 0,
        'MAX_BATHROOMS': 20,
        'MIN_PARKING': 0,
        'MAX_PARKING': 10
    },
    'BUILDING': {
        'MIN_FLOOR': -10,        # Subterráneo -10
        'MAX_FLOOR': 200,        # Piso 200 máximo
        'MIN_UNITS': 1,          # 1 unidad mínima
        'MAX_UNITS': 10000       # 10,000 unidades máximo
    }
}

# Mensajes de error comunes
ERROR_MESSAGES = {
    'INVALID_TAX_ID': 'Identificador fiscal inválido',
    'INVALID_EMAIL': 'Email inválido',
    'INVALID_PHONE': 'Teléfono inválido',
    'INVALID_PRICE': 'Precio inválido',
    'INVALID_AREA': 'Área inválida',
    'INVALID_COORDINATES': 'Coordenadas inválidas',
    'DUPLICATE_UNIT': 'Número de unidad duplicado',
    'UNIT_NOT_AVAILABLE': 'Unidad no disponible',
    'INVALID_STATUS_CHANGE': 'Cambio de estado inválido'
}

# Configuración de API
API_CONFIG = {
    'VERSION': '1.0.0',
    'TITLE': 'API Proyectos Inmobiliarios',
    'DESCRIPTION': 'API para gestión de proyectos inmobiliarios y stock',
    'MAX_REQUEST_SIZE': 50 * 1024 * 1024,  # 50MB
    'REQUEST_TIMEOUT': 30  # 30 segundos
}

# Headers de respuesta
RESPONSE_HEADERS = {
    'API_VERSION': 'X-API-Version',
    'REQUEST_ID': 'X-Request-ID',
    'RATE_LIMIT': 'X-RateLimit-Limit',
    'RATE_LIMIT_REMAINING': 'X-RateLimit-Remaining'
}

# Orientaciones de la unidad
ORIENTATION_TYPES = [
    'norte',
    'sur',
    'este',
    'oeste',
    'noreste',
    'noroeste',
    'sureste',
    'suroeste',
    'este-oeste',
    'norte-sur'
]