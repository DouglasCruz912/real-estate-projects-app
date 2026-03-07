# Estructura del Proyecto API Proyectos Inmobiliarios

Este documento describe la arquitectura y organización del código del proyecto API de Proyectos Inmobiliarios.

## 🏗️ Arquitectura General

El proyecto sigue una **arquitectura en capas** con separación clara de responsabilidades:

```
┌─────────────────┐
│   Presentation  │  ← Routers (FastAPI endpoints)
├─────────────────┤
│    Business     │  ← Services (lógica de negocio)
├─────────────────┤
│   Data Access   │  ← Models & Database (SQLAlchemy)
├─────────────────┤
│  Infrastructure │  ← External services (S3, Redis)
└─────────────────┘
```

## 📁 Estructura de Directorios

### Directorio Raíz (`apis/api-projects/`)

```
apis/api-projects/
├── src/                    # Código fuente principal
├── docs/                   # Documentación del proyecto
├── main.py                 # Aplicación FastAPI principal
├── start.py                # Script de inicio con configuración
├── requirements.txt        # Dependencias del proyecto
├── .env.example           # Plantilla de variables de entorno
├── .gitignore             # Archivos ignorados por Git
├── README.md              # Documentación principal
├── STRUCTURE.md           # Este archivo
├── CHANGELOG.md           # Historial de cambios
└── TODO.md                # Tareas pendientes
```

### Directorio Source (`src/`)

```
src/
├── __init__.py            # Inicialización del módulo
├── database/              # Configuración de base de datos
├── models/                # Modelos SQLAlchemy (entidades)
├── schemas/               # Esquemas Pydantic (validación)
├── routers/               # Endpoints FastAPI (controladores)
├── services/              # Lógica de negocio
├── dependencies/          # Dependencias reutilizables
├── middleware/            # Middleware personalizado
└── utils/                 # Utilidades generales
```

## 📊 Detalle por Componente

### 1. Database (`src/database/`)

**Propósito**: Configuración y gestión de conexiones a base de datos.

```
database/
├── __init__.py           # Exportaciones principales
├── base.py               # Modelo base SQLAlchemy
├── config.py             # Configuración de BD y variables
└── connection.py         # Gestión de conexiones async
```

**Responsabilidades**:
- Configuración de conexión MySQL
- Gestión de sesiones asíncronas
- Configuración de Redis (opcional)
- Creación automática de tablas

### 2. Models (`src/models/`)

**Propósito**: Definición de entidades de base de datos.

```
models/
├── __init__.py           # Exportaciones de modelos
└── models.py             # Todos los modelos SQLAlchemy
```

**Entidades**:
- `RealEstateCompany`: Empresas inmobiliarias
- `Project`: Proyectos inmobiliarios
- `ProjectStock`: Unidades de stock
- `LegalUser`: Representantes legales
- `ProjectImage`: Imágenes de proyectos

### 3. Schemas (`src/schemas/`)

**Propósito**: Validación y serialización de datos con Pydantic.

```
schemas/
├── __init__.py           # Exportaciones de schemas
├── base.py               # Esquemas base reutilizables
├── companies.py          # Schemas para inmobiliarias
├── projects.py           # Schemas para proyectos
├── stock.py              # Schemas para stock
└── searches.py           # Schemas para búsquedas
```

**Tipos de Schemas**:
- `Create`: Para creación de recursos
- `Update`: Para actualización parcial
- `Response`: Para respuestas de la API
- `Search`: Para filtros de búsqueda

### 4. Routers (`src/routers/`)

**Propósito**: Definición de endpoints HTTP (controladores).

```
routers/
├── __init__.py           # Router principal
├── companies.py          # CRUD inmobiliarias
├── projects.py           # CRUD proyectos
├── stock.py              # CRUD stock
├── searches.py           # Endpoints de búsqueda
└── files.py              # Gestión de archivos S3
```

**Características**:
- Autenticación via API Key
- Validación automática con Pydantic
- Documentación OpenAPI automática
- Manejo de errores centralizado

### 5. Services (`src/services/`)

**Propósito**: Lógica de negocio y operaciones complejas.

```
services/
├── __init__.py           # Exportaciones de servicios
├── company_service.py    # Lógica de inmobiliarias
├── project_service.py    # Lógica de proyectos
├── stock_service.py      # Lógica de stock
└── s3_service.py         # Operaciones con AWS S3
```

**Responsabilidades**:
- Operaciones CRUD complejas
- Validaciones de negocio
- Interacción con servicios externos
- Transformación de datos

### 6. Dependencies (`src/dependencies/`)

**Propósito**: Dependencias reutilizables para FastAPI.

```
dependencies/
├── __init__.py           # Exportaciones principales
├── auth_dependencies.py # Validación de API Key
└── db_dependencies.py   # Dependencias de base de datos
```

**Dependencias Principales**:
- `RequireAPIKey`: Autenticación obligatoria
- `DatabaseDep`: Sesión de base de datos
- `validate_api_key`: Validación de API Key

### 7. Middleware (`src/middleware/`)

**Propósito**: Middleware personalizado para la aplicación.

```
middleware/
├── __init__.py           # Exportaciones
└── auth.py               # Middleware de logging
```

**Funcionalidades**:
- Logging de requests/responses
- Medición de tiempo de respuesta
- Headers de CORS

### 8. Utils (`src/utils/`)

**Propósito**: Utilidades y helpers generales.

```
utils/
├── __init__.py           # Exportaciones
└── helpers.py            # Funciones auxiliares
```

## 🔄 Flujo de Datos

### Request Flow (Entrada)

```
1. Cliente HTTP Request
   ↓
2. Middleware (logging, CORS)
   ↓  
3. Router (endpoint, validación)
   ↓
4. Dependencies (auth, DB session)
   ↓
5. Service (lógica de negocio)
   ↓
6. Model/Database (persistencia)
```

### Response Flow (Salida)

```
1. Database Response
   ↓
2. Service (transformación)
   ↓
3. Schema (serialización)
   ↓
4. Router (HTTP response)
   ↓
5. Middleware (logging)
   ↓
6. Cliente HTTP Response
```

## 🔧 Patrones de Diseño

### 1. Repository Pattern (Implícito)

Los servicios actúan como repositorios, encapsulando el acceso a datos:

```python
# Servicio como Repository
async def get_company_by_id(db: AsyncSession, company_id: int):
    # Encapsula la lógica de acceso a datos
    return await db.get(RealEstateCompany, company_id)
```

### 2. Dependency Injection

FastAPI maneja automáticamente las dependencias:

```python
@router.get("/companies/{company_id}")
async def get_company(
    company_id: int,
    db: DatabaseDep,  # Inyección automática
    _: RequireAPIKey  # Inyección de autenticación
):
    return await company_service.get_company_by_id(db, company_id)
```

### 3. Strategy Pattern (Servicios)

Diferentes servicios implementan estrategias específicas:

```python
# Estrategia para inmobiliarias
company_service.create_company()

# Estrategia para proyectos  
project_service.create_project()
```

### 4. Builder Pattern (Schemas)

Los schemas Pydantic construyen objetos validados:

```python
class CompanyCreate(BaseModel):
    name: str
    email: EmailStr
    # Construcción validada automática
```

## 📋 Convenciones de Código

### Nomenclatura

- **Archivos**: `snake_case.py`
- **Clases**: `PascalCase`
- **Funciones**: `snake_case`
- **Variables**: `snake_case`
- **Constantes**: `UPPER_CASE`

### Estructura de Funciones

```python
async def function_name(
    required_param: Type,
    optional_param: Type = None,
    db: DatabaseDep,
    auth: RequireAPIKey
) -> ReturnType:
    """
    Descripción clara de la función
    
    Args:
        required_param: Descripción del parámetro
        optional_param: Parámetro opcional
    
    Returns:
        Descripción del retorno
    
    Raises:
        APIException: Cuando ocurre un error
    """
    # Implementación
```

### Manejo de Errores

```python
from fastapi import HTTPException

# Error estándar
raise HTTPException(
    status_code=404,
    detail="Recurso no encontrado"
)

# Error con contexto
raise HTTPException(
    status_code=400,
    detail=f"El proyecto {project_id} no existe"
)
```

## 🚀 Escalabilidad

### Horizontal

- **Stateless**: La API no mantiene estado
- **Database pooling**: Conexiones reutilizables
- **Cache ready**: Preparado para Redis
- **S3 integration**: Almacenamiento externo

### Vertical

- **Async/await**: Operaciones no bloqueantes
- **Connection pooling**: Reutilización de conexiones
- **Lazy loading**: Carga bajo demanda
- **Paginación**: Resultados limitados

## 🧪 Testing

### Estructura de Tests

```
tests/
├── test_routers/         # Tests de endpoints
├── test_services/        # Tests de lógica de negocio  
├── test_models/          # Tests de modelos
└── conftest.py           # Configuración de tests
```

### Patrones de Testing

- **Unit tests**: Servicios individuales
- **Integration tests**: Endpoints completos
- **Database tests**: Con base de datos temporal
- **Mock tests**: Servicios externos (S3, Redis)
