# API Proyectos Inmobiliarios

Una API REST moderna para la gestión de proyectos inmobiliarios, desarrollada con FastAPI y diseñada para ser simple y mantenible.

## 📋 Características

- **🏗️ Gestión de Proyectos**: CRUD completo para proyectos inmobiliarios
- **🏢 Inmobiliarias**: Administración de empresas desarrolladoras
- **📦 Control de Stock**: Gestión de unidades disponibles y vendidas
- **🔍 Búsquedas Avanzadas**: Filtros personalizables para encontrar propiedades
- **📁 Gestión de Archivos**: Subida y manejo de imágenes y documentos via AWS S3 o MinIO
- **🔐 Autenticación Simple**: Protección via API Key
- **📊 Health Check**: Monitoreo del estado de servicios

## 🚀 Tecnologías

- **Framework**: FastAPI 0.104.1
- **Base de Datos**: MySQL 8.0 con SQLAlchemy 2.0 (async)
- **Validación**: Pydantic 2.5.0
- **Almacenamiento**: AWS S3 o MinIO (S3 compatible) para archivos
- **Logging**: Structlog para logs estructurados
- **Python**: 3.8+

## 📂 Estructura del Proyecto

Ver descripción detallada en [STRUCTURE.md](STRUCTURE.md).

```
backend/
├── src/
│   ├── database/          # Configuración y conexión a BD
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Esquemas Pydantic para validación
│   ├── routers/           # Endpoints de la API
│   ├── services/          # Lógica de negocio
│   ├── dependencies/      # Dependencias reutilizables
│   ├── middleware/        # Middleware personalizado
│   └── utils/             # Utilidades generales
├── main.py                # Aplicación FastAPI principal
├── start.py               # Script de inicio rápido
├── docker-compose.yml     # MySQL 8.0 + MinIO
└── requirements.txt       # Dependencias del proyecto
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- Docker (para MySQL y MinIO via `docker-compose up -d`)
- Cuenta AWS con acceso a S3 **o** MinIO local (para imágenes y documentos)

### Pasos de Instalación

1. **Clonar y navegar al proyecto**
```bash
cd backend
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Levantar servicios (MySQL + MinIO)**
```bash
docker-compose up -d
```

5. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto (backend)
cp .env.example .env
# Editar .env con tus credenciales (DB_*, API_KEY, AWS_S3_*)
```

### Variables de Entorno Requeridas

Copiar desde `.env.example` y ajustar valores. Resumen:

```env
# Base de datos (coincidir con docker-compose.yml)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=real_estate_app
DB_USER=app_user
DB_PASSWORD=app_password

# API
API_KEY=tu-api-key-secreta

# AWS S3 (imágenes y documentos)
AWS_S3_ACCESS_KEY=tu_access_key_id
AWS_S3_SECRET_KEY=tu_secret_access_key
AWS_S3_REGION=us-west-2
AWS_S3_BUCKET_NAME=bucket-api-projects
```

### Desarrollo local con MinIO (S3 compatible, sin AWS)

Puedes usar MinIO en Docker como S3 local para probar subida de imágenes y documentos sin cuenta AWS:

1. **Levantar servicios** (MySQL + MinIO):
```bash
docker-compose up -d
```

2. **En tu `.env`** configura el endpoint y credenciales de MinIO:
```env
AWS_S3_ENDPOINT_URL=http://localhost:9000
AWS_S3_ACCESS_KEY=minioadmin
AWS_S3_SECRET_KEY=minioadmin
AWS_S3_REGION=us-east-1
AWS_S3_BUCKET_NAME=bucket-api-projects
```

3. El bucket `bucket-api-projects` se crea automáticamente al iniciar la API si no existe.

4. **Consola MinIO:** http://localhost:9001 (usuario `minioadmin`, contraseña `minioadmin`) para ver archivos subidos.

## 🚀 Uso

### Iniciar el Servidor

**Opción 1: Script de inicio rápido (recomendado)**
```bash
python start.py
```

**Opción 2: Uvicorn directo**
```bash
uvicorn main:app --reload --host localhost --port 8000
```

### Acceder a la Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔐 Autenticación

Todos los endpoints (excepto `/`, `/health`, `/docs`) requieren el header `X-API-Key`. Ejemplo:

```bash
curl -H "X-API-Key: tu-api-key" http://localhost:8000/api/companies
```

## 📡 Endpoints Principales

Prefijo base: `/api`.

### Inmobiliarias (`/api/companies`)
- `GET /api/companies` - Listar inmobiliarias
- `POST /api/companies` - Crear inmobiliaria
- `GET /api/companies/{id}` - Obtener inmobiliaria
- `PUT /api/companies/{id}` - Actualizar inmobiliaria
- `DELETE /api/companies/{id}` - Eliminar inmobiliaria (soft delete)

### Proyectos (`/api/projects`)
- `GET /api/projects` - Listar proyectos (paginado)
- `POST /api/projects` - Crear proyecto
- `GET /api/projects/{id}` - Obtener proyecto
- `PUT /api/projects/{id}` - Actualizar proyecto
- `DELETE /api/projects/{id}` - Eliminar proyecto (soft delete)
- `GET /api/projects/{id}/details` - Ficha comercial (proyecto + stock)

### Stock (`/api/stock`)
- `GET /api/stock/project/{project_id}` - Listar stock de un proyecto
- `POST /api/stock` - Crear unidad de stock
- `GET /api/stock/{id}` - Obtener unidad
- `PUT /api/stock/{id}` - Actualizar unidad
- `DELETE /api/stock/{id}` - Eliminar unidad (soft delete)

### Archivos (`/api/files`) — S3
- `POST /api/files/project/{project_id}/images` - Subir imágenes de proyecto
- `GET /api/files/project/{project_id}/images` - Listar imágenes
- `GET /api/files/project/{project_id}/images/summary` - Resumen de imágenes
- `PUT /api/files/project-image/{id}` - Actualizar imagen
- `DELETE /api/files/project-image/{id}` - Eliminar imagen
- `POST /api/files/project/{project_id}/documents` - Subir documento
- `GET /api/files/project/{project_id}/documents` - Listar documentos
- `PUT /api/files/project-document/{id}` - Actualizar documento
- `DELETE /api/files/project-document/{id}` - Eliminar documento

## 💡 Ejemplos de Uso

### Crear una Inmobiliaria

```bash
curl -X POST "http://localhost:8000/api/companies" \
  -H "X-API-Key: tu-api-key" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Inmobiliaria Ejemplo\", \"email\": \"contacto@ejemplo.com\", \"phone\": \"+56912345678\", \"city\": \"Santiago\", \"is_active\": true}"
```

### Listar proyectos (paginado)

```bash
curl "http://localhost:8000/api/projects?skip=0&limit=10" -H "X-API-Key: tu-api-key"
```

## 🏗️ Desarrollo

### Ejecutar Tests

```bash
pytest
```

### Estructura de Base de Datos

El proyecto maneja las siguientes entidades principales (detalle en [STRUCTURE.md](STRUCTURE.md)):

- **RealEstateCompany**: Inmobiliarias desarrolladoras
- **Project**: Proyectos inmobiliarios
- **ProjectStock**: Unidades de stock por proyecto
- **LegalUser**: Representantes legales de proyectos
- **ProjectImage**: Imágenes de proyectos (almacenadas en S3)
- **ProjectDocument**: Documentos de proyectos (almacenados en S3)

### Agregar Nuevos Endpoints

1. Crear router en `src/routers/`
2. Implementar lógica en `src/services/`
3. Definir schemas en `src/schemas/`
4. Agregar al router principal en `src/routers/__init__.py`

## 🔧 Configuración Avanzada

### Variables de Entorno Opcionales

```env
# Logging
LOG_LEVEL=INFO
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Para soporte y preguntas:

- 📋 Issues: [GitHub Issues](https://github.com/tu-org/api-projects/issues)
- 📖 Documentación: [Wiki del Proyecto](https://github.com/tu-org/api-projects/wiki)

## 🎯 Roadmap

- [ ] Implementar autenticación OAuth2
- [ ] Agregar cache con Redis para consultas frecuentes
- [ ] Implementar notificaciones por email
- [ ] Crear dashboard de métricas
- [ ] Agregar exportación a Excel
- [ ] Implementar sistema de audit logs
