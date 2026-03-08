# Contexto General - API Proyectos y Stock

> **Estructura implementada:** La estructura real del backend está en [STRUCTURE.md](../STRUCTURE.md). La siguiente era la propuesta inicial.

## 📋 Objetivo del MVP
Crear un sistema de gestión centralizado para proyectos inmobiliarios y su stock asociado, reemplazando el flujo actual basado en Google Drive + SyncStock.

## 🗂️ Estructura de Carpetas Sugerida (FastAPI) — referencia histórica

```
apis/api-projects/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación FastAPI principal
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py            # Configuración SQLAlchemy
│   │   ├── settings.py            # Variables de entorno
│   │   └── auth.py                # Middleware de autenticación
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # Modelo base SQLAlchemy
│   │   ├── project.py             # Modelo de proyecto
│   │   ├── stock.py               # Modelo de stock
│   │   ├── user.py                # Modelo de usuarios
│   │   └── associations.py        # Tablas de relación many-to-many
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── project.py             # Pydantic schemas para proyectos
│   │   ├── stock.py               # Pydantic schemas para stock
│   │   ├── user.py                # Pydantic schemas para usuarios
│   │   └── responses.py           # Schemas de respuesta
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── projects.py            # Endpoints de proyectos
│   │   ├── stock.py               # Endpoints de stock
│   │   ├── users.py               # Endpoints de usuarios
│   │   └── health.py              # Health checks
│   ├── services/
│   │   ├── __init__.py
│   │   ├── project_service.py     # Lógica de negocio proyectos
│   │   ├── stock_service.py       # Lógica de negocio stock
│   │   └── user_service.py        # Lógica de negocio usuarios
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py     # Repositorio base
│   │   ├── project_repository.py  # Acceso a datos proyectos
│   │   └── stock_repository.py    # Acceso a datos stock
│   └── utils/
│       ├── __init__.py
│       ├── exceptions.py          # Excepciones personalizadas
│       ├── validators.py          # Validadores custom
│       └── helpers.py             # Funciones auxiliares
├── tests/
│   ├── __init__.py
│   ├── conftest.py               # Configuración pytest
│   ├── test_projects.py          # Tests proyectos
│   └── test_stock.py             # Tests stock
├── requirements.txt
├── Dockerfile
└── README.md
```

## 📊 Campos Principales

### Proyecto
- **General**: name, legal_name, rut, company, fechas, estado, consolidado, ejecutivo, descripción
- **Contacto**: teléfono, web, redes sociales, brochure
- **Ubicación**: dirección, región, coordenadas, Google Maps
- **Arquitecto**: datos completos del profesional
- **Representantes**: array de objetos con datos legales

### Stock
- **General**: project_id, tipo, subtipo, número, descripción, estado, bloqueado, compartido
- **Atributos**: piso, orientación, etapa, dormitorios, baños, estacionamientos
- **Superficies**: 15+ tipos diferentes de medidas
- **Precios**: valores base, lista, venta, habilitación

## ⚠️ Aclaraciones Importantes

### Impacto en Sistemas Críticos
La implementación de esta API afectará directamente:

1. **Sistema de Reservas** - Debe mantener compatibilidad con IDs existentes
2. **Gestión de Negocios** - Dependencias con stock_id y project_id
3. **Sistema de Favoritos** - Referencias a proyectos deben mantenerse
4. **Reportes y Analytics** - Queries existentes deben seguir funcionando
5. **Integraciones Externas** - APIs que consumen datos de proyectos

### Estrategia de Migración
- **Fase 1**: Crear nueva API manteniendo IDs existentes
- **Fase 2**: Migración progresiva de datos
- **Fase 3**: Desactivación gradual de sistemas legacy (SyncStock, AppServices)
- **Fase 4**: Cleanup de código y optimizaciones

### Consideraciones Técnicas
- Implementar soft deletes para mantener integridad referencial
- Mantener compatibilidad con esquemas de BD existentes
- Versionado de API para transiciones sin downtime
- Logs detallados para troubleshooting durante migración
- Rollback plan en caso de issues críticos

### Usuarios Beta
- Lanzamiento inicial con grupo reducido de KAMs
- Feedback continuo para refinamiento
- Métricas de adopción y performance
- Plan de escalamiento gradual
