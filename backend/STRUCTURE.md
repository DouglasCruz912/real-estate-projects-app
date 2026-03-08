# Estructura del Proyecto - API Proyectos Inmobiliarios

Arquitectura y organización del backend.

## Arquitectura General

El proyecto sigue una **arquitectura en capas** con separación de responsabilidades:

```
┌─────────────────┐
│   Presentation  │  ← Routers (FastAPI endpoints)
├─────────────────┤
│    Business     │  ← Services (lógica de negocio)
├─────────────────┤
│   Data Access   │  ← Models & Database (SQLAlchemy async)
├─────────────────┤
│  Infrastructure │  ← External services (S3)
└─────────────────┘
```

## Estructura de Directorios

### Raíz (`backend/`)

```
backend/
├── src/                    # Código fuente principal
├── docker/                 # Archivos Docker
│   └── init/               # Scripts SQL de inicialización
│       └── 01-schema.sql   # Schema completo de la BD
├── docs/                   # Documentación del proyecto
├── main.py                 # Aplicación FastAPI principal
├── start.py                # Script de inicio con configuración
├── docker-compose.yml      # Docker Compose para MySQL
├── requirements.txt        # Dependencias Python
├── .env.example            # Plantilla de variables de entorno
├── README.md               # Documentación principal
├── STRUCTURE.md            # Este archivo
├── CHANGELOG.md            # Historial de cambios
└── TODO.md                 # Tareas pendientes
```

### Source (`src/`)

```
src/
├── __init__.py
├── database/               # Configuración de base de datos
│   ├── base.py             # Modelo base SQLAlchemy
│   ├── config.py           # Variables de configuración
│   └── connection.py       # Conexiones async (engine, sessions)
├── models/                 # Modelos SQLAlchemy (entidades)
│   └── models.py           # Todos los modelos
├── schemas/                # Esquemas Pydantic (validación)
│   ├── base.py             # BaseResponse, PaginatedResponse, etc.
│   ├── companies.py        # CompanyCreate, CompanyUpdate, CompanyResponse
│   ├── projects.py         # ProjectCreateRequest, ProjectResponse, etc.
│   ├── stock.py            # StockCreateRequest, StockResponse, etc.
│   ├── users.py            # UserCreate, UserUpdate, UserResponse
│   └── project_image.py    # Schemas de imágenes
├── routers/                # Endpoints FastAPI
│   ├── __init__.py         # main_router que agrupa todos
│   ├── companies.py        # /api/companies
│   ├── projects.py         # /api/projects
│   ├── stock.py            # /api/stock
│   └── files.py            # /api/files (imágenes y documentos)
├── services/               # Lógica de negocio
│   ├── company_service.py
│   ├── project_service.py
│   ├── stock_service.py
│   ├── user_service.py
│   ├── s3_service.py
│   ├── project_image_service.py
│   └── project_document_service.py
├── dependencies/           # Dependencias inyectables
│   ├── auth_dependencies.py  # RequireAPIKey
│   └── db_dependencies.py    # DatabaseDep
├── middleware/
│   └── auth.py             # SimpleLoggingMiddleware
└── utils/
    ├── exceptions.py       # Jerarquía de excepciones (APIException → subclases)
    ├── validation.py
    ├── helpers.py
    └── constants.py
```

## Entidades (Modelos)

| Modelo | Tabla | Descripción |
|--------|-------|-------------|
| `User` | `users` | Usuarios de la aplicación (auth, auditoría) |
| `RealEstateCompany` | `real_estate_companies` | Empresas inmobiliarias |
| `Project` | `projects` | Proyectos inmobiliarios |
| `ProjectStock` | `project_stock` | Unidades individuales de cada proyecto |
| `LegalUser` | `legal_users` | Representantes legales de proyectos |
| `ProjectImage` | `project_images` | Imágenes asociadas a proyectos |
| `ProjectDocument` | `project_documents` | Documentos asociados a proyectos |
| `ProjectCommercial` | `project_commercial` | Información comercial (1:1 con Project) |

Todos los modelos (excepto `User`) incluyen campos de auditoría: `created_by`, `updated_by`, `deleted_by` (FK a `users.id`) y soft delete via `deleted_at`.

## Flujo de Datos

```
Request → Middleware (logging) → Router (validación) → Dependencies (auth, DB)
    → Service (lógica) → Model/Database → Response Schema → HTTP Response
```

**Regla clave**: Los routers solo reciben, delegan al service y retornan. Toda la lógica de negocio vive en los services.

## Patrones de Diseño

### Inyección de Dependencias

```python
@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(
    company_id: int,
    db: AsyncSession = DatabaseDep,
    _: bool = RequireAPIKey
):
    company = await company_service.get_company_by_id(db, company_id)
    return CompanyResponse.model_validate(company)
```

### Jerarquía de Excepciones

```
APIException (HTTPException)
├── NotFoundError (404)
│   ├── ProjectNotFoundError
│   ├── CompanyNotFoundError
│   └── StockUnitNotFoundError
├── ValidationError (422)
├── ConflictError (409)
│   ├── DuplicateProjectError
│   └── DuplicateCompanyError
├── BusinessLogicError (400)
│   ├── InvalidStockStatusError
│   └── StockNotAvailableError
├── AuthenticationError (401)
├── AuthorizationError (403)
├── DatabaseError (500)
└── CacheError (503)
```

## Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| Framework | FastAPI |
| Servidor | Uvicorn |
| ORM | SQLAlchemy 2.0 (async con aiomysql) |
| Base de datos | MySQL 8.0 (Docker) |
| Validación | Pydantic v2 |
| Auth | API Key (header `X-API-Key`) |
| Almacenamiento | AWS S3 (imágenes y documentos) |
| Logging | structlog |
| Deploy | AWS Lambda (Mangum) |
| Tests | pytest, pytest-asyncio, httpx |

## Docker

Levantar la base de datos:

```bash
docker-compose up -d
```

El script `docker/init/01-schema.sql` crea automáticamente todas las tablas al iniciar el contenedor por primera vez.

## Convenciones

- **Archivos**: `snake_case.py`
- **Clases/Modelos**: `PascalCase`
- **Funciones/Variables**: `snake_case`
- **Schemas**: `EntityCreate`, `EntityUpdate`, `EntityResponse` por entidad
- **Services**: funciones auxiliares privadas con prefijo `_`
- **Soft delete**: filtrar siempre por `deleted_at.is_(None)`
- **Queries**: estilo SQLAlchemy 2.0 (`select()`, `update()`, `delete()`)
