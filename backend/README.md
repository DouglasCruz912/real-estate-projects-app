# API Proyectos Inmobiliarios

Una API REST moderna para la gestión de proyectos inmobiliarios, desarrollada con FastAPI y diseñada para ser simple y mantenible.

## 📋 Características

- **🏗️ Gestión de Proyectos**: CRUD completo para proyectos inmobiliarios
- **🏢 Inmobiliarias**: Administración de empresas desarrolladoras
- **📦 Control de Stock**: Gestión de unidades disponibles y vendidas
- **🔍 Búsquedas Avanzadas**: Filtros personalizables para encontrar propiedades
- **📁 Gestión de Archivos**: Subida y manejo de imágenes via AWS S3
- **🔐 Autenticación Simple**: Protección via API Key
- **📊 Health Check**: Monitoreo del estado de servicios

## 🚀 Tecnologías

- **Framework**: FastAPI 0.104.1
- **Base de Datos**: MySQL con SQLAlchemy 2.0 (async)
- **Cache**: Redis 5.0.1 (opcional)
- **Validación**: Pydantic 2.5.0
- **Almacenamiento**: AWS S3 para archivos
- **Logging**: Structlog para logs estructurados
- **Python**: 3.8+

## 📂 Estructura del Proyecto

```
apis/api-projects/
├── src/
│   ├── database/          # Configuración y conexión a BD
│   ├── models/            # Modelos SQLAlchemy
│   ├── schemas/           # Esquemas Pydantic para validación
│   ├── routers/           # Endpoints de la API
│   ├── services/          # Lógica de negocio
│   ├── dependencies/      # Dependencias reutilizables
│   ├── middleware/        # Middleware personalizado
│   └── utils/             # Utilidades generales
├── main.py               # Aplicación FastAPI principal
├── start.py              # Script de inicio rápido
└── requirements.txt      # Dependencias del proyecto
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- MySQL 8.0+
- Redis (opcional)
- Cuenta AWS con acceso a S3

### Pasos de Instalación

1. **Clonar y navegar al proyecto**
```bash
cd apis/api-projects
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

4. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto
cp .env.example .env
```

### Variables de Entorno Requeridas

```env
# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=real_estate_app
DB_USER=root
DB_PASSWORD=tu_password

# Redis (opcional)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=

# API Key
API_KEY=tu-api-key-secreta

# AWS S3 (para archivos)
AWS_ACCESS_KEY_ID=tu_access_key
AWS_SECRET_ACCESS_KEY=tu_secret_key
AWS_REGION=us-west-2
S3_BUCKET_IMAGES=proyectos-images
S3_BUCKET_DOCUMENTS=proyectos-documents
```

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

Todos los endpoints están protegidos con API Key. Para hacer peticiones:

```bash
curl -H "X-API-Key: tu-api-key" http://localhost:8000/api/v1/companies
```

## 📡 Endpoints Principales

### Inmobiliarias
- `GET /api/v1/companies` - Listar inmobiliarias
- `POST /api/v1/companies` - Crear inmobiliaria
- `GET /api/v1/companies/{id}` - Obtener inmobiliaria
- `PUT /api/v1/companies/{id}` - Actualizar inmobiliaria
- `DELETE /api/v1/companies/{id}` - Eliminar inmobiliaria

### Proyectos
- `GET /api/v1/projects` - Listar proyectos
- `POST /api/v1/projects` - Crear proyecto
- `GET /api/v1/projects/{id}` - Obtener proyecto
- `PUT /api/v1/projects/{id}` - Actualizar proyecto
- `DELETE /api/v1/projects/{id}` - Eliminar proyecto

### Stock
- `GET /api/v1/stock` - Listar unidades
- `POST /api/v1/stock` - Crear unidad
- `GET /api/v1/stock/{id}` - Obtener unidad
- `PUT /api/v1/stock/{id}` - Actualizar unidad
- `DELETE /api/v1/stock/{id}` - Eliminar unidad

### Búsquedas
- `GET /api/v1/search/projects` - Buscar proyectos con filtros
- `GET /api/v1/search/stock` - Buscar unidades con filtros

### Archivos
- `POST /api/v1/files/upload` - Subir archivo a S3
- `DELETE /api/v1/files` - Eliminar archivo de S3

## 💡 Ejemplos de Uso

### Crear una Inmobiliaria

```bash
curl -X POST "http://localhost:8000/api/v1/companies" \
  -H "X-API-Key: tu-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Inmobiliaria Ejemplo",
    "email": "contacto@ejemplo.com",
    "phone": "+56912345678",
    "city": "Santiago",
    "is_active": true
  }'
```

### Buscar Proyectos

```bash
curl "http://localhost:8000/api/v1/search/projects?city=Santiago&price_min=50000000" \
  -H "X-API-Key: tu-api-key"
```

## 🏗️ Desarrollo

### Ejecutar Tests

```bash
pytest
```

### Estructura de Base de Datos

El proyecto maneja las siguientes entidades principales:

- **RealEstateCompany**: Inmobiliarias desarrolladoras
- **Project**: Proyectos inmobiliarios
- **ProjectStock**: Unidades individuales de cada proyecto
- **LegalUser**: Representantes legales de proyectos
- **ProjectImage**: Imágenes asociadas a proyectos

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

# Cache Redis (opcional)
REDIS_PASSWORD=password_redis

# AWS adicional
AWS_DEFAULT_REGION=us-west-2
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
