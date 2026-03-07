"""
Utilidades de validación personalizada
"""

import re
from typing import Any, Optional, Tuple
from decimal import Decimal


def validate_rut(rut: str) -> Tuple[bool, str]:
    """Validar formato de RUT chileno con mensaje descriptivo"""
    
    if not rut:
        return False, "El RUT es requerido"
    
    # Limpiar espacios
    rut = rut.strip()
    
    if not rut:
        return False, "El RUT no puede estar vacío"
    
    # Limpiar formato
    rut_clean = re.sub(r'[^0-9kK]', '', rut.upper())
    
    if len(rut_clean) < 8 or len(rut_clean) > 9:
        return False, "El RUT debe tener entre 8 y 9 caracteres"
    
    # Verificar que tenga solo números y K al final
    if not rut_clean[:-1].isdigit():
        return False, "El RUT debe contener solo números antes del dígito verificador"
    
    if rut_clean[-1] not in '0123456789K':
        return False, "El dígito verificador debe ser un número o la letra K"
    
    # Separar número y dígito verificador
    rut_number = rut_clean[:-1]
    check_digit = rut_clean[-1]
    
    # Calcular dígito verificador
    multiplier = 2
    total = 0
    
    # Multiplicar cada dígito por la secuencia 2,3,4,5,6,7,2,3,4,5,6,7...
    for digit in reversed(rut_number):
        total += int(digit) * multiplier
        multiplier = 2 if multiplier == 7 else multiplier + 1
    
    # Calcular dígito verificador según algoritmo chileno
    remainder = total % 11
    dv = 11 - remainder
    
    # Casos especiales: si dv es 11 -> 0, si dv es 10 -> K
    if dv == 11:
        calculated_digit = '0'
    elif dv == 10:
        calculated_digit = 'K'
    else:
        calculated_digit = str(dv)
    
    if check_digit != calculated_digit:
        return False, "El dígito verificador del RUT no es válido"
    
    return True, "RUT válido"


def validate_email(email: str) -> Tuple[bool, str]:
    """Validar formato de email con mensaje descriptivo"""
    
    if not email:
        return False, "El email es requerido"
    
    # Limpiar espacios
    email = email.strip()
    
    if not email:
        return False, "El email no puede estar vacío"
    
    # Verificar que contenga exactamente un @
    if email.count('@') != 1:
        if '@' not in email:
            return False, "El email debe contener el símbolo '@'"
        else:
            return False, "El email debe contener exactamente un '@'"
    
    # Dividir en parte local y dominio
    local_part, domain = email.split('@')
    
    # Validar que ambas partes existan
    if not local_part:
        return False, "Debe especificar un usuario antes del '@'"
    
    if not domain:
        return False, "Debe especificar un dominio después del '@'"
    
    # Validar que el dominio tenga al menos un punto
    if '.' not in domain:
        return False, "El dominio debe contener un punto (ej: dominio.com)"
    
    # Validar con regex básico pero efectivo
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "El formato del email no es válido"
    
    return True, "Email válido"


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validar formato de teléfono chileno con mensaje descriptivo"""
    
    if not phone:
        return False, "El teléfono es requerido"
    
    # Limpiar espacios
    phone = phone.strip()
    
    if not phone:
        return False, "El teléfono no puede estar vacío"
    
    # Limpiar formato
    phone_clean = re.sub(r'[^0-9+]', '', phone)
    
    if not phone_clean:
        return False, "El teléfono debe contener números"
    
    # Formatos válidos:
    # +56912345678 (celular con código país)
    # 912345678 (celular)
    # +56221234567 (fijo con código país)
    # 221234567 (fijo)
    
    patterns = [
        r'^\+569\d{8}$',  # +56912345678
        r'^9\d{8}$',      # 912345678
        r'^\+562\d{8}$',  # +56221234567
        r'^2\d{8}$'       # 221234567
    ]
    
    if any(re.match(pattern, phone_clean) for pattern in patterns):
        return True, "Teléfono válido"
    else:
        return False, "Formato de teléfono inválido. Formatos válidos: +56912345678, 912345678, +56221234567, 221234567"


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
    """Validar coordenadas geográficas"""
    
    try:
        lat = float(latitude)
        lng = float(longitude)
        
        # Rango válido para Chile
        return (-56.0 <= lat <= -17.0) and (-110.0 <= lng <= -66.0)
    except (ValueError, TypeError):
        return False


# Funciones de compatibilidad que retornan solo bool
def validate_rut_simple(rut: str) -> bool:
    """Validación simple de RUT (solo bool para compatibilidad)"""
    result, _ = validate_rut(rut)
    return result

def validate_phone_simple(phone: str) -> bool:
    """Validación simple de teléfono (solo bool para compatibilidad)"""
    result, _ = validate_phone(phone)
    return result

def normalize_rut(rut: str) -> Optional[str]:
    """Normalizar formato de RUT"""
    
    if not rut:
        return None
    
    # Limpiar y validar
    rut_clean = re.sub(r'[^0-9kK]', '', rut.upper())
    
    if not validate_rut_simple(rut_clean):
        return None
    
    # Formatear como 12345678-9
    if len(rut_clean) == 8:
        return f"{rut_clean[:-1]}-{rut_clean[-1]}"
    else:
        return f"{rut_clean[:-1]}-{rut_clean[-1]}"


def normalize_phone(phone: str) -> Optional[str]:
    """Normalizar formato de teléfono"""
    
    if not phone:
        return None
    
    # Limpiar formato
    phone_clean = re.sub(r'[^0-9+]', '', phone)
    
    if not validate_phone_simple(phone_clean):
        return None
    
    # Normalizar a formato internacional
    if phone_clean.startswith('+56'):
        return phone_clean
    elif phone_clean.startswith('9') and len(phone_clean) == 9:
        return f"+56{phone_clean}"
    elif phone_clean.startswith('2') and len(phone_clean) == 9:
        return f"+56{phone_clean}"
    
    return phone_clean


