"""
Funciones auxiliares para la API
"""

import uuid
import hashlib
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from decimal import Decimal


def generate_request_id() -> str:
    """Generar ID único para request"""
    return str(uuid.uuid4())


def generate_cache_key(*args: Any) -> str:
    """Generar clave de cache basada en argumentos"""
    key_string = "_".join(str(arg) for arg in args)
    return hashlib.md5(key_string.encode()).hexdigest()


def format_price(price: Optional[Decimal], currency: str = "CLP") -> str:
    """Formatear precio con moneda"""
    if price is None:
        return "Precio a consultar"
    
    if currency == "CLP":
        return f"${price:,.0f}"
    elif currency == "UF":
        return f"{price:,.1f} UF"
    else:
        return f"{price:,.2f} {currency}"


def format_area(area: Optional[Decimal]) -> str:
    """Formatear área en m²"""
    if area is None:
        return "Área a consultar"
    
    return f"{area:,.1f} m²"


def format_datetime(dt: Optional[datetime]) -> Optional[str]:
    """Formatear datetime a string ISO"""
    if dt is None:
        return None
    
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt.isoformat()


def parse_datetime(dt_string: str) -> Optional[datetime]:
    """Parsear string ISO a datetime"""
    try:
        return datetime.fromisoformat(dt_string)
    except (ValueError, TypeError):
        return None


def clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Limpiar diccionario removiendo valores None"""
    return {k: v for k, v in data.items() if v is not None}


def merge_dicts(*dicts: Dict[str, Any]) -> Dict[str, Any]:
    """Fusionar múltiples diccionarios"""
    result = {}
    for d in dicts:
        if d:
            result.update(d)
    return result


def paginate_results(
    items: List[Any], 
    page: int = 1, 
    per_page: int = 100
) -> Dict[str, Any]:
    """Paginar lista de resultados"""
    
    total = len(items)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    
    paginated_items = items[start_idx:end_idx]
    
    return {
        "items": paginated_items,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": (total + per_page - 1) // per_page,
            "has_next": end_idx < total,
            "has_prev": page > 1
        }
    }


def calculate_percentage(part: int, total: int) -> float:
    """Calcular porcentaje"""
    if total == 0:
        return 0.0
    return round((part / total) * 100, 2)


def safe_divide(numerator: Any, denominator: Any, default: float = 0.0) -> float:
    """División segura evitando división por cero"""
    try:
        num = float(numerator)
        den = float(denominator)
        
        if den == 0:
            return default
        
        return num / den
        
    except (ValueError, TypeError):
        return default


def format_file_size(size_bytes: int) -> str:
    """Formatear tamaño de archivo"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncar texto con sufijo"""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def generate_slug(text: str) -> str:
    """Generar slug URL-friendly"""
    import re
    
    # Convertir a minúsculas
    slug = text.lower()
    
    # Reemplazar espacios y caracteres especiales con guiones
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'[\s-]+', '-', slug)
    
    # Remover guiones al inicio y final
    slug = slug.strip('-')
    
    return slug


def extract_numbers(text: str) -> List[int]:
    """Extraer todos los números de un texto"""
    import re
    return [int(match) for match in re.findall(r'\d+', text)]


def is_valid_uuid(uuid_string: str) -> bool:
    """Validar si string es UUID válido"""
    try:
        uuid.UUID(uuid_string)
        return True
    except (ValueError, TypeError):
        return False


def deep_get(dictionary: Dict[str, Any], keys: str, default: Any = None) -> Any:
    """Obtener valor anidado usando notación de puntos"""
    keys_list = keys.split('.')
    
    for key in keys_list:
        if isinstance(dictionary, dict) and key in dictionary:
            dictionary = dictionary[key]
        else:
            return default
    
    return dictionary


def deep_set(dictionary: Dict[str, Any], keys: str, value: Any) -> None:
    """Establecer valor anidado usando notación de puntos"""
    keys_list = keys.split('.')
    
    for key in keys_list[:-1]:
        if key not in dictionary:
            dictionary[key] = {}
        dictionary = dictionary[key]
    
    dictionary[keys_list[-1]] = value


def batch_process(items: List[Any], batch_size: int = 100):
    """Procesar lista en lotes"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


def retry_on_exception(max_attempts: int = 3, delay: float = 1.0):
    """Decorator para reintentar función en caso de excepción"""
    import time
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    time.sleep(delay * (attempt + 1))
            
        return wrapper
    return decorator


def get_client_ip(headers: Dict[str, str]) -> str:
    """Extraer IP del cliente desde headers"""
    
    # Verificar headers de proxy
    forwarded_for = headers.get("x-forwarded-for")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = headers.get("x-real-ip")
    if real_ip:
        return real_ip
    
    return "unknown"


def mask_sensitive_data(data: str, visible_chars: int = 4) -> str:
    """Enmascarar datos sensibles"""
    if len(data) <= visible_chars:
        return "*" * len(data)
    
    masked_part = "*" * (len(data) - visible_chars)
    visible_part = data[-visible_chars:]
    
    return masked_part + visible_part


def validate_coordinates(coordinates: Dict[str, Any]) -> Dict[str, Any]:
    """Validar y normalizar coordenadas geográficas"""
    if not coordinates or not isinstance(coordinates, dict):
        raise ValueError("coordinates must be a dictionary")
    
    # Verificar que tenga lat y lng
    if 'lat' not in coordinates or 'lng' not in coordinates:
        raise ValueError("coordinates must contain 'lat' and 'lng' keys")
    
    try:
        lat = float(coordinates['lat'])
        lng = float(coordinates['lng'])
        
        # Rango válido para Chile
        if not (-56.0 <= lat <= -17.0):
            raise ValueError("latitude must be between -56.0 and -17.0 (valid range for Chile)")
        
        if not (-110.0 <= lng <= -66.0):
            raise ValueError("longitude must be between -110.0 and -66.0 (valid range for Chile)")
        
        return {
            'lat': lat,
            'lng': lng
        }
        
    except (ValueError, TypeError) as e:
        if isinstance(e, ValueError) and "must be between" in str(e):
            raise e
        raise ValueError("coordinates must contain valid numeric lat and lng values") 