"""
Utilidades de validación personalizada
"""

import re
from typing import Any, Optional, Tuple
from decimal import Decimal


def validate_tax_id(tax_id: str) -> Tuple[bool, str]:
    """Validar formato genérico de identificador fiscal (alfanumérico, guiones, puntos)"""
    if not tax_id:
        return False, "El identificador fiscal es requerido"

    tax_id = tax_id.strip()
    if not tax_id:
        return False, "El identificador fiscal no puede estar vacío"

    if len(tax_id) < 4 or len(tax_id) > 20:
        return False, "El identificador fiscal debe tener entre 4 y 20 caracteres"

    if not re.match(r'^[A-Za-z0-9.\-]+$', tax_id):
        return False, "El identificador fiscal solo puede contener letras, números, puntos y guiones"

    return True, "Identificador fiscal válido"


def validate_email(email: str) -> Tuple[bool, str]:
    """Validar formato de email con mensaje descriptivo"""
    if not email:
        return False, "El email es requerido"

    email = email.strip()
    if not email:
        return False, "El email no puede estar vacío"

    if email.count('@') != 1:
        if '@' not in email:
            return False, "El email debe contener el símbolo '@'"
        else:
            return False, "El email debe contener exactamente un '@'"

    local_part, domain = email.split('@')

    if not local_part:
        return False, "Debe especificar un usuario antes del '@'"
    if not domain:
        return False, "Debe especificar un dominio después del '@'"
    if '.' not in domain:
        return False, "El dominio debe contener un punto (ej: dominio.com)"

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "El formato del email no es válido"

    return True, "Email válido"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validar formato de teléfono internacional genérico"""
    if not phone:
        return False, "El teléfono es requerido"

    phone = phone.strip()
    if not phone:
        return False, "El teléfono no puede estar vacío"

    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)

    if not re.match(r'^\+?\d{7,15}$', phone_clean):
        return False, "Formato de teléfono inválido. Use formato internacional (ej: +1234567890) o solo dígitos (mín 7, máx 15)"

    return True, "Teléfono válido"


def validate_price(price: Any) -> bool:
    """Validar precio válido"""
    try:
        decimal_price = Decimal(str(price))
        return decimal_price >= 0
    except (ValueError, TypeError):
        return False


def validate_area(area: Any) -> bool:
    """Validar área válida"""
    try:
        decimal_area = Decimal(str(area))
        return decimal_area > 0
    except (ValueError, TypeError):
        return False


def validate_coordinates(latitude: Any, longitude: Any) -> bool:
    """Validar coordenadas geográficas (rango mundial)"""
    try:
        lat = float(latitude)
        lng = float(longitude)
        return (-90.0 <= lat <= 90.0) and (-180.0 <= lng <= 180.0)
    except (ValueError, TypeError):
        return False


def validate_tax_id_simple(tax_id: str) -> bool:
    """Validación simple de identificador fiscal (solo bool)"""
    result, _ = validate_tax_id(tax_id)
    return result


def validate_phone_simple(phone: str) -> bool:
    """Validación simple de teléfono (solo bool)"""
    result, _ = validate_phone(phone)
    return result


def normalize_phone(phone: str) -> Optional[str]:
    """Normalizar formato de teléfono"""
    if not phone:
        return None

    phone_clean = re.sub(r'[\s\-\(\)]', '', phone)

    if not validate_phone_simple(phone_clean):
        return None

    return phone_clean
