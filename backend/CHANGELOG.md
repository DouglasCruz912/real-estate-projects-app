# Changelog

Todas las mejoras notables de la API de Proyectos Inmobiliarios se documentan aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere al [Versionado Semántico](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-07-30 - Expansión de Campos de Proyecto y Comerciales ✨

### ✨ Nuevas Funcionalidades

#### 🏗️ Campos de Tipo de Proyecto
- **Tipo de Proyecto**: Nuevo campo `type` para categorizar proyectos (departamentos, casas, oficinas, etc.)
- **Tipo de Entrega**: Nuevo campo `delivery_type` para especificar modalidad de entrega (inmediata, verde, blanco, etc.)
- **Precio Único**: Nuevo campo `unique_price` para proyectos con precio fijo sin rango

#### 🎯 Campos de Promoción y Destacado
- **Proyecto Foco**: Nuevo campo `is_promo` para marcar proyectos promocionales/foco
- **Proyecto Destacado**: Nuevo campo `is_hot` para marcar proyectos destacados por demanda o características especiales

#### 💰 Campos Comerciales Expandidos
- **Abono Inicial**: Nuevo campo `initial_payment` para porcentaje de pie requerido (0-100%)
- **Cuotón**: Nuevo campo `big_down_payment` para monto de cuotón en la moneda del proyecto
- **Notas de Arriendo**: Nuevo campo `notes_rent` para información adicional sobre condiciones de arriendo

### 🔧 Cambios Técnicos

#### 📊 Modelos Actualizados
- **Project Model**: Agregados 5 nuevos campos (`type`, `delivery_type`, `unique_price`, `is_promo`, `is_hot`)
- **ProjectCommercial Model**: Agregados 3 nuevos campos comerciales (`initial_payment`, `big_down_payment`, `notes_rent`)

#### 🌐 Schemas API Actualizados
- **ProjectCreateRequest**: Soporte para nuevos campos en creación
- **ProjectUpdateRequest**: Soporte para actualización de nuevos campos
- **ProjectResponse**: Incluye todos los nuevos campos en respuestas

#### 🗄️ Base de Datos
- **8 Columnas Nuevas**: 5 en tabla `projects`, 3 en tabla `project_commercial`
- **7 Índices Nuevos**: Para optimizar consultas en nuevos campos
- **Migración SQL**: Script `20250130 - Agregar nuevos campos a projects y project_commercial.sql`

#### ⚙️ Servicios Actualizados
- **Separación de Datos**: Función `_separate_project_and_commercial_data` actualizada
- **Combinación de Datos**: Función `_combine_project_and_commercial_data` expandida
- **Compatibilidad**: Mantiene retrocompatibilidad con clientes existentes

### 📋 Campos Detallados

#### Proyecto Base (`projects`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `type` | VARCHAR(100) | Tipo de proyecto inmobiliario |
| `delivery_type` | VARCHAR(100) | Modalidad de entrega del proyecto |
| `unique_price` | DECIMAL(15,2) | Precio único para proyectos sin rango |
| `is_promo` | BOOLEAN | Proyecto foco/promocional |
| `is_hot` | BOOLEAN | Proyecto destacado por demanda o características especiales |

#### Información Comercial (`project_commercial`)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `initial_payment` | DECIMAL(5,2) | Porcentaje de abono inicial (0-100%) |
| `big_down_payment` | DECIMAL(15,2) | Monto del cuotón |
| `notes_rent` | TEXT | Notas adicionales sobre arriendo |

## [1.1.1] - 2025-07-30 - Simplificación de Estado de Stock 🔧

### 🗑️ Campos Eliminados

#### 🏠 Simplificación del Modelo de Estado
- **Eliminación de Campos Redundantes**: Removidos campos booleanos `is_available`, `is_reserved`, `is_sold`
- **Estado Unificado**: Toda la información de estado se maneja únicamente a través del campo `status`
- **Mejor Consistencia**: Eliminación de posibles inconsistencias entre campos booleanos y estado

### 🔧 Cambios Técnicos

#### 📊 Modelos y Schemas Actualizados
- **ProjectStock Model**: Eliminados 3 campos booleanos de estado
- **StockCreateRequest**: Removidos campos redundantes de estado
- **StockUpdateRequest**: Simplificado para usar solo campo `status`
- **StockResponse**: Respuesta limpia con estado unificado
- **StockStateUpdate**: Simplificado a solo campo `status`

#### 🗄️ Base de Datos
- **3 Columnas Eliminadas**: `is_available`, `is_reserved`, `is_sold`
- **Índice Eliminado**: `idx_stock_available`
- **Migración SQL**: Script `20250130 - Eliminar campos booleanos de estado en project_stock.sql`

#### 🔍 Lógica de Negocio Actualizada
- **Filtros por Disponibilidad**: Ahora usan `status = 'available'`
- **Ordenamiento**: Prioriza unidades disponibles usando el campo `status`
- **Agregaciones**: Estadísticas de proyecto calculadas desde campo `status`
- **Validaciones**: Eliminación de unidades vendidas basada en `status = 'sold'`

### 🚀 Beneficios
- **Menor Complejidad**: Un solo campo para gestionar estado
- **Mejor Consistencia**: Eliminación de estados contradictorios
- **Mantenimiento Simplificado**: Menos campos a sincronizar
- **Performance**: Menor tamaño de tabla y consultas más simples

### 📝 Notas de Migración
1. Ejecutar script de migración SQL para eliminar columnas
2. Las aplicaciones que usen los campos eliminados deben actualizarse para usar solo `status`
3. Los valores válidos de `status` son: `available`, `reserved`, `sold`, `blocked`

### ⚠️ Cambios Incompatibles
- **API Breaking**: Respuestas ya no incluyen campos `is_available`, `is_reserved`, `is_sold`
- **Requests**: Los campos eliminados en requests serán ignorados
- **Filtros**: Filtros por `available_only` ahora usan `status = 'available'`

## [1.1.0] - 2025-01-30 - Expansión de Campos de Stock 📊

### ✨ Nuevas Características

#### 🏠 Modelo de Stock Ampliado
- **Descripción de Unidades**: Campo de texto libre para descripción detallada de cada unidad
- **Orientación**: Campo para especificar orientación de la unidad (norte, sur, este, oeste, etc.)
- **Información de Estacionamientos**: Campo específico para detalles de estacionamientos asignados

#### 📐 Superficies Detalladas
- **Superficie Interna**: Área interior construida en m²
- **Superficie de Terraza**: Área de terrazas y balcones en m²
- **Superficie de Jardín**: Área de jardín privado en m²
- **Superficie de Despensa**: Área de almacenamiento/despensa en m²
- **Superficie Multiuso Asignable**: Áreas comunes asignables en m²
- **Superficie Útil**: Superficie real utilizable en m²
- **Superficie de Terreno**: Área total del terreno en m²
- **Otras Superficies**: Superficies adicionales no categorizadas en m²

#### 💰 Sistema de Precios Ampliado
- **Moneda**: Campo para especificar moneda (CLP, UF, USD, EUR)
- **Precio de Lista**: Precio oficial publicado
- **Descuentos**: Monto de descuento aplicado
- **Valor Habilitado**: Precio final habilitado para venta
- **Precio Promocional**: Precio especial por promociones
- **Bonos**: Bonificaciones aplicables al precio

### 🔧 Mejoras Técnicas

#### 📊 Schemas Actualizados
- **StockCreateRequest**: Ampliado con todos los nuevos campos
- **StockUpdateRequest**: Soporte para actualización de campos adicionales
- **StockResponse**: Respuesta completa con toda la información expandida
- **StockFilters**: Filtros avanzados por orientación, superficies y precios

#### 🔍 Validaciones Mejoradas
- **Validación de Moneda**: Solo monedas permitidas (CLP, UF, USD, EUR)
- **Validación de Orientación**: Orientaciones geográficas válidas
- **Validación de Superficies**: Valores numéricos positivos
- **Validación de Precios**: Valores monetarios consistentes

#### 🗄️ Base de Datos
- **17 Nuevas Columnas**: Agregadas a la tabla `project_stock`
- **Índices Optimizados**: Nuevos índices para campos frecuentemente consultados
- **Comentarios**: Documentación completa de todos los campos
- **Migración SQL**: Script de migración `20250130 - Agregar campos adicionales tabla project_stock.sql`

### 🚀 Compatibilidad
- **Retrocompatibilidad**: Todos los campos existentes mantienen su funcionamiento
- **Campos Opcionales**: Los nuevos campos son opcionales para no romper integraciones existentes
- **Valores por Defecto**: Campos con valores por defecto apropiados



## [1.0.0] - 2025-07-11 - MVP Release 🚀

### 🎯 Primera Versión Mínima Viable (MVP)

Esta es la primera versión estable de la API de Proyectos Inmobiliarios, diseñada para ser simple, mantenible y lista para producción.

### ✨ Features Implementadas

#### 🏢 Gestión de Inmobiliarias
- **CRUD completo**: Crear, leer, actualizar y eliminar inmobiliarias
- **Validación de datos**: RUT, email, teléfono con formato chileno
- **Estados**: Activo/inactivo, verificado/no verificado
- **Búsqueda**: Por nombre, ciudad, estado de verificación

#### 🏗️ Gestión de Proyectos
- **CRUD completo**: Administración total de proyectos inmobiliarios
- **Información detallada**: Ubicación, precios, fechas de entrega
- **Estados del proyecto**: En desarrollo, en venta, entregado, cancelado
- **Relaciones**: Vinculación con inmobiliarias desarrolladoras
- **Métricas**: Unidades totales vs disponibles

#### 📦 Control de Stock
- **Gestión de unidades**: Departamentos, casas, locales comerciales
- **Características detalladas**: Dormitorios, baños, superficie, piso
- **Estados de venta**: Disponible, reservado, vendido
- **Precios**: Valor base en CLP y UF
- **Extras**: Estacionamiento, bodega

#### 🔍 Sistema de Búsquedas
- **Filtros avanzados**: Por ciudad, precio, tipo, características
- **Búsqueda de proyectos**: Filtros por inmobiliaria, estado, ubicación
- **Búsqueda de stock**: Por proyecto, precio, dormitorios, superficie
- **Paginación**: Resultados limitados para mejor rendimiento

#### 📁 Gestión de Archivos
- **Integración S3**: Subida de imágenes y documentos a AWS
- **Tipos de archivo**: Imágenes de proyectos, documentos legales
- **Validación**: Tipos de archivo y tamaños permitidos
- **URLs seguras**: Links temporales para acceso a archivos

#### 👥 Representantes Legales
- **Contactos del proyecto**: Administración de representantes
- **Información completa**: Datos personales y profesionales
- **Múltiples contactos**: Varios representantes por proyecto
- **Contacto principal**: Designación de representante primario

### 🔧 Arquitectura Técnica

#### 🛠️ Stack Tecnológico
- **Framework**: FastAPI 0.104.1 con async/await
- **Base de Datos**: MySQL 8.0+ con SQLAlchemy 2.0 (async)
- **Cache**: Redis 5.0.1 (opcional)
- **Validación**: Pydantic 2.5.0 con schemas robustos
- **Almacenamiento**: AWS S3 para archivos e imágenes
- **Logging**: Structlog para logs estructurados
- **Documentación**: OpenAPI/Swagger automático

#### 🏗️ Arquitectura de Software
- **Capas separadas**: Presentation, Business, Data Access
- **Patrón Repository**: Servicios encapsulan acceso a datos
- **Dependency Injection**: FastAPI maneja dependencias automáticamente
- **Async everywhere**: Operaciones no bloqueantes en toda la aplicación

#### 🔐 Seguridad y Autenticación
- **API Key simple**: Autenticación via header `X-API-Key`
- **Protección total**: Todos los endpoints requieren autenticación
- **CORS configurado**: Acceso desde frontend permitido
- **Validación robusta**: Pydantic valida todos los inputs
- **Logs de seguridad**: Registro de todas las operaciones

#### 📊 Base de Datos
- **5 Entidades principales**:
  - `RealEstateCompany`: Inmobiliarias desarrolladoras
  - `Project`: Proyectos inmobiliarios
  - `ProjectStock`: Unidades individuales
  - `LegalUser`: Representantes legales
  - `ProjectImage`: Imágenes de proyectos
- **Relaciones bien definidas**: Foreign keys con integridad referencial
- **Índices optimizados**: Para consultas frecuentes
- **Soft deletes**: Eliminación lógica para auditoría

### 🚀 Endpoints API

#### Inmobiliarias (`/api/v1/companies`)
- `GET /` - Listar inmobiliarias con filtros
- `POST /` - Crear nueva inmobiliaria
- `GET /{id}` - Obtener inmobiliaria específica
- `PUT /{id}` - Actualizar inmobiliaria
- `DELETE /{id}` - Eliminar inmobiliaria

#### Proyectos (`/api/v1/projects`)
- `GET /` - Listar proyectos con filtros
- `POST /` - Crear nuevo proyecto
- `GET /{id}` - Obtener proyecto específico
- `PUT /{id}` - Actualizar proyecto
- `DELETE /{id}` - Eliminar proyecto
- `GET /{id}/stats` - Estadísticas del proyecto

#### Stock (`/api/v1/stock`)
- `GET /` - Listar unidades con filtros
- `POST /` - Crear nueva unidad
- `GET /{id}` - Obtener unidad específica
- `PUT /{id}` - Actualizar unidad
- `DELETE /{id}` - Eliminar unidad
- `PUT /{id}/status` - Cambiar estado (disponible/reservado/vendido)

#### Búsquedas (`/api/v1/search`)
- `GET /projects` - Buscar proyectos con filtros avanzados
- `GET /stock` - Buscar unidades con filtros avanzados

#### Archivos (`/api/v1/files`)
- `POST /upload` - Subir archivo a S3
- `DELETE /` - Eliminar archivo de S3

### 🛠️ Herramientas de Desarrollo

#### 📋 Scripts Incluidos
- `start.py` - Inicio rápido con configuración automática
- `main.py` - Aplicación FastAPI principal
- Health check automático de servicios
- Creación automática de tablas al inicio

#### 📖 Documentación
- **Swagger UI**: Documentación interactiva en `/docs`
- **ReDoc**: Documentación alternativa en `/redoc`
- **README completo**: Guía de instalación y uso
- **STRUCTURE.md**: Documentación de arquitectura
- **CHANGELOG.md**: Historial de versiones

#### 🧪 Testing Ready
- Configuración de pytest incluida
- Tests asíncronos con pytest-asyncio
- Cobertura de código con pytest-cov
- Cliente HTTP de pruebas con httpx

### 🎛️ Configuración y Deployment

#### ⚙️ Variables de Entorno
- Base de datos MySQL configurable
- Redis opcional para cache
- AWS S3 para almacenamiento
- API Key personalizable
- Logs configurables

#### 🐳 Deployment Ready
- Requirements.txt completo
- Configuración para entornos múltiples
- Scripts de inicio incluidos
- Health checks integrados

### 📈 Métricas y Monitoring

#### 📊 Health Checks
- Estado de MySQL
- Estado de Redis (opcional)
- Estado general de la aplicación
- Versión de la API

#### 📝 Logging
- Logs estructurados con Structlog
- Registro de requests/responses
- Tiempo de ejecución de endpoints
- Errores y excepciones detalladas

### 🎯 Características de Calidad

#### ✅ Código Limpio
- Arquitectura en capas bien definida
- Separación clara de responsabilidades
- Patrones de diseño consistentes
- Nomenclatura descriptiva y consistente

#### 🔒 Robustez
- Validación exhaustiva de datos
- Manejo centralizado de errores
- Transacciones de base de datos
- Logging completo para debugging

#### ⚡ Performance
- Operaciones asíncronas en toda la aplicación
- Connection pooling para base de datos
- Paginación en listados grandes
- Optimización de consultas SQL

#### 🧪 Mantenibilidad
- Código simple y legible
- Documentación completa
- Tests preparados
- Estructura modular

### 🎊 Resultado Final

Esta primera versión MVP de la API de Proyectos Inmobiliarios proporciona:

- ✅ **Funcionalidad completa** para gestión de proyectos inmobiliarios
- ✅ **Arquitectura robusta** y escalable
- ✅ **Documentación completa** para desarrolladores
- ✅ **Seguridad implementada** con autenticación
- ✅ **Performance optimizado** con async/await
- ✅ **Código mantenible** con buenas prácticas
- ✅ **Deployment ready** para producción

**🚀 La API está lista para uso en producción y desarrollo futuro.**

## [1.1.0] - 2025-07-24 - Expansión del Modelo de Proyectos 🏗️

### 🎯 Separación Arquitectónica + Unificación de API

Esta versión implementa una importante expansión del modelo de proyectos, separando la información en dos modelos especializados mientras mantiene una API unificada para el frontend.

### ✨ Nuevas Características

#### 🏢 Modelo de Proyectos Expandido
- **11 campos nuevos en `Project`**: 
  - `executive` - Ejecutivo responsable del proyecto
  - `executive_email` - Email del ejecutivo responsable
  - `delivery_end_date` - Fecha de entrega final (diferente a delivery_date)
  - `launch_date` - Fecha de lanzamiento del proyecto
  - `phone` - Teléfono principal de contacto
  - `website` - Sitio web oficial del proyecto
  - `country` - País donde se ubica el proyecto
  - `postal_code` - Código postal
  - `url_google_maps` - URL de ubicación en Google Maps
  - `latitude` - Coordenada GPS de latitud
  - `longitude` - Coordenada GPS de longitud

- **Campo `description` convertido a JSON**: Permite almacenar información estructurada como resúmenes, destacados, características del edificio, etc.

#### 🏪 Nuevo Modelo ProjectCommercial
- **Separación arquitectónica**: Información comercial/marketing separada del core del proyecto
- **23 campos comerciales especializados**:

**Información de Postventa (3 campos)**:
- `after_sales_email` - Email del equipo de postventa
- `after_sales_executive` - Ejecutivo responsable de postventa  
- `after_sales_phone` - Teléfono de postventa

**Información Financiera (7 campos)**:
- `finances_insurance_company` - Compañía aseguradora
- `finances_insurance_policy` - Póliza de seguro
- `finances_insured_value` - Valor asegurado total
- `finances_insured_value_util` - Valor asegurado de utilidad
- `finances_benefit` - Beneficio financiero
- `finances_annual_rate` - Tasa anual
- `finances_credit_rate` - Tasa de crédito

**Información Comercial Variable (9 campos)**:
- `down_payment_bonus` - Información de bono pie
- `reservation` - Condiciones de reserva
- `pre_approval` - Información de pre-aprobación
- `installments` - Sistema de cuotas
- `balloon_payment` - Información de cuotón
- `annual_capital_gain` - Plusvalía anual estimada
- `construction_capital_gain` - Plusvalía durante construcción
- `vacancy` - Información de vacancia
- `additional_information` - Información adicional del proyecto

**Campos JSON Flexibles (4 campos)**:
- `social_networks` - URLs de redes sociales y tour virtual
- `payment_plan_conditions` - Condiciones detalladas de pago
- `promotions_benefits` - Promociones actuales y beneficios
- `frequently_asked_questions` - Preguntas frecuentes

#### 🔗 Relación One-to-One
- **Vinculación automática**: `Project` ↔ `ProjectCommercial` via `project_id`
- **Cascada de eliminación**: Al eliminar proyecto, se elimina información comercial
- **Índices optimizados**: Para consultas eficientes entre modelos

### 🛠️ Mejoras Técnicas

#### 🎯 API Unificada
- **CRUD consolidado**: Toda la información (proyecto + comercial) se maneja via endpoints `/projects`
- **Payload único**: Un solo schema para crear/actualizar toda la información
- **Separación interna**: El servicio separa automáticamente los datos entre modelos
- **Respuesta combinada**: Las respuestas incluyen toda la información unificada

#### 🏗️ Arquitectura Mejorada
- **Separación de responsabilidades**: Core del proyecto vs información comercial/marketing
- **Performance optimizada**: Consultas más eficientes al separar datos frecuentes vs esporádicos
- **Escalabilidad**: Facilita agregar nuevos campos comerciales sin afectar el modelo principal
- **Mantenibilidad**: Código más organizado con responsabilidades claras

#### 🔧 Servicios Refactorizados
- **Funciones helper internas**:
  - `_separate_project_and_commercial_data()` - Separa payload entrante
  - `_combine_project_and_commercial_data()` - Combina datos para respuesta
- **Transacciones atómicas**: Creación/actualización de ambos modelos en una sola transacción
- **Carga automática**: Siempre incluye información comercial en las respuestas

### 🗄️ Cambios de Base de Datos

#### 📊 Migración Completa
- **Script de migración**: `20250122 - Project Commercial Model Expansion.sql`
- **11 columnas nuevas en `projects`**
- **Nueva tabla `project_commercial`** con 21 campos + auditoría de usuarios
- **Índices optimizados**: Para mejorar performance de consultas
- **Constraints de integridad**: Foreign keys y validaciones

#### 🔍 Índices Agregados
- **En `projects`**: `executive`, `executive_email`, `country`, `phone`, `website`, `delivery_end_date`, `launch_date`
- **En `project_commercial`**: `project_id`, `after_sales_executive`, `created_by`, `updated_by`

### 📋 Schemas Actualizados

#### 🎯 Schemas Unificados
- **`ProjectCreateRequest`**: Incluye todos los 34 campos (11 core + 23 comerciales)
- **`ProjectUpdateRequest`**: Todos los campos opcionales para updates parciales
- **`ProjectResponse`**: Respuesta unificada con toda la información
- **Eliminados**: Schemas comerciales separados (ya no necesarios)

#### ✅ Validaciones Mejoradas
- **Campos JSON**: Validación de estructura para `description`, `social_networks`, etc.
- **Fechas coherentes**: `delivery_end_date` debe ser posterior a `delivery_date`
- **Precios lógicos**: `price_to` debe ser mayor a `price_from`
- **Estados válidos**: Validación contra constantes definidas

### 🚀 Endpoints Actualizados

#### 📡 Comportamiento Unificado
- **`POST /projects`**: Crea proyecto + información comercial en una sola operación
- **`PUT /projects/{id}`**: Actualiza ambos modelos según campos enviados
- **`GET /projects/{id}`**: Respuesta siempre incluye información comercial
- **`GET /projects`**: Lista incluye información comercial de todos los proyectos

#### 🗑️ Endpoints Eliminados
- Removidos endpoints comerciales separados (`/projects/{id}/commercial`)
- API más simple y consistente

### 🎛️ Compatibilidad

#### ✅ Backward Compatible
- **Campos existentes**: Mantienen mismo comportamiento
- **Campos nuevos**: Todos opcionales, no rompe integraciones existentes
- **Respuestas**: Incluyen campos nuevos como `null` si no están definidos

#### 🔄 Migración Suave
- **Datos existentes**: Se mantienen intactos
- **Campos JSON**: `description` migra automáticamente
- **Información comercial**: Se crea bajo demanda

### 📈 Beneficios de la Implementación

#### 🏗️ Arquitectónicos
- **Separación clara**: Core vs comercial/marketing
- **Escalabilidad**: Fácil agregar nuevos campos comerciales
- **Performance**: Consultas más eficientes
- **Mantenibilidad**: Código más organizado

#### 🎯 Para Desarrolladores
- **API simple**: Un solo endpoint para toda la información
- **Payloads flexibles**: Solo enviar campos que cambian
- **Respuestas completas**: Toda la información en una respuesta
- **Documentación clara**: Schemas bien documentados

#### 🚀 Para el Negocio
- **Información rica**: 34 campos para describir proyectos completamente
- **Flexibilidad**: Campos JSON para información variable
- **Trazabilidad**: Auditoría de usuarios completa
- **Escalabilidad**: Preparado para crecimiento futuro

### 🎊 Resultado Final

Esta versión 1.1.0 transforma la API de proyectos en una solución más robusta y escalable:

- ✅ **34 campos totales** para información completa de proyectos
- ✅ **Arquitectura separada** pero API unificada
- ✅ **Performance optimizada** con modelos especializados  
- ✅ **Backward compatible** con integraciones existentes
- ✅ **Preparada para escalar** con nuevos requerimientos
- ✅ **Documentación actualizada** con ejemplos completos

**🚀 La API ahora soporta información comercial completa manteniendo simplicidad de uso.**
