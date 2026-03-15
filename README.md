# Real Estate Projects App

App full-stack de gestión de proyectos inmobiliarios. Backend en FastAPI (Python) y frontend en Next.js (React/TypeScript).

## Descripción

Sistema centralizado para administrar proyectos inmobiliarios, inmobiliarias, stock de unidades, imágenes y documentos. Incluye autenticación JWT, subida de archivos a S3/MinIO y documentación OpenAPI.

## Características

- **Inmobiliarias**: CRUD de empresas desarrolladoras
- **Proyectos**: Gestión de proyectos con filtros, paginación y ficha comercial
- **Stock**: Unidades por proyecto (disponibles, vendidas, bloqueadas)
- **Archivos**: Imágenes y documentos por proyecto (AWS S3 o MinIO)
- **Usuarios y roles**: Autenticación JWT, login y gestión de usuarios (admin)
- **API REST**: Documentación Swagger/ReDoc, health check

## Stack tecnológico

| Capa      | Tecnologías |
|-----------|-------------|
| **Backend** | FastAPI, Python 3.8+, SQLAlchemy 2 (async), MySQL 8, Pydantic v2, JWT, Boto3 (S3), Structlog |
| **Frontend** | Next.js 16, React 19, TypeScript, TanStack Query, React Hook Form, Zod, Tailwind CSS, shadcn/ui |
| **Infra** | Docker (MySQL + MinIO), AWS S3 o MinIO compatible S3 |

## Estructura del proyecto

```
├── backend/                 # API FastAPI
│   ├── src/
│   │   ├── database/        # Configuración y conexión BD
│   │   ├── models/          # Modelos SQLAlchemy
│   │   ├── schemas/         # Schemas Pydantic
│   │   ├── routers/         # Endpoints (auth, companies, projects, stock, files, users)
│   │   ├── services/        # Lógica de negocio
│   │   ├── dependencies/    # Auth (JWT), BD
│   │   └── utils/           # Excepciones, validación, helpers
│   ├── docker/              # Scripts init BD
│   ├── docs/                # Documentación
│   ├── main.py
│   ├── docker-compose.yml   # MySQL 8 + MinIO
│   ├── requirements.txt
│   └── .env.example
├── frontend/                # App Next.js
│   ├── src/
│   │   ├── app/             # Rutas (dashboard, companies, projects, stock, users)
│   │   ├── components/      # UI, formularios, tablas, layout
│   │   ├── contexts/        # AuthContext
│   │   ├── hooks/           # useCompanies, useProjects, etc.
│   │   └── providers/       # QueryProvider
│   ├── package.json
│   └── .env.local (crear desde ejemplo)
└── README.md
```

## Requisitos previos

- **Python 3.8+** (backend)
- **Node.js 18+** (frontend)
- **Docker y Docker Compose** (MySQL y MinIO)
- Cuenta **AWS** (opcional; se puede usar MinIO local)

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/real-estate-projects-app.git
cd real-estate-projects-app
```

### 2. Backend

```bash
cd backend

# Entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
# source venv/bin/activate

# Dependencias
pip install -r requirements.txt

# Variables de entorno
cp .env.example .env
# Editar .env con DB_*, JWT_*, AWS_S3_* (o MinIO)

# Levantar MySQL y MinIO
docker-compose up -d

# Iniciar API
python start.py
# o: uvicorn main:app --reload --host localhost --port 8000
```

- **Documentación API**: http://localhost:8000/docs  
- **Health**: http://localhost:8000/health  

### 3. Frontend

```bash
cd frontend

# Dependencias
npm install

# Variables de entorno: crear .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000
# NEXT_PUBLIC_API_KEY=opcional-si-api-key

# Desarrollo
npm run dev
```

- **App**: http://localhost:3000  

### Uso de MinIO (S3 local, sin AWS)

En `backend/.env`:

```env
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_S3_ACCESS_KEY=minioadmin
AWS_S3_SECRET_KEY=minioadmin
AWS_S3_REGION=us-east-1
AWS_S3_BUCKET_NAME=projects
```

Consola MinIO: http://localhost:9001 (minioadmin / minioadmin).

## Autenticación

- **Login**: `POST /api/auth/login` con `email` y `password`; devuelve un JWT.
- El frontend guarda el token y lo envía en el header `Authorization: Bearer <token>`.
- Endpoints protegidos requieren JWT válido (y en algunos casos rol admin).

## Scripts útiles

| Ubicación   | Comando        | Descripción        |
|------------|----------------|--------------------|
| Backend    | `python start.py` | Inicia la API      |
| Backend    | `pytest`       | Tests              |
| Frontend   | `npm run dev`  | Servidor desarrollo |
| Frontend   | `npm run build`| Build producción   |

## Documentación adicional

- **Backend**: [backend/README.md](backend/README.md) — endpoints, variables de entorno, ejemplos.
- **Estructura backend**: [backend/STRUCTURE.md](backend/STRUCTURE.md) — capas, modelos, convenciones.

## Licencia

Este proyecto está bajo la Licencia MIT.
