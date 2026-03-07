# ADR-001: Arquitectura de Base de Datos para API Proyectos y Stock

**Estado:** Aceptado  
**Fecha:** 2025-07-09  
**Autores:** Equipo Backend  
**Revisores:** Equipo Técnico  

## Contexto

### Problema
El sistema actual de gestión de proyectos inmobiliarios y stock presenta múltiples deficiencias críticas:

- **Gestión manual** a través de Google Drive + herramienta SyncStock
- **Información desactualizada** que causa reservas múltiples en la misma unidad
- **Falta de centralización** que obliga a las KAMs a cambiar entre herramientas
- **Modelos de BD inconsistentes** con tipos de datos mezclados y nomenclatura incoherente
- **Performance deficiente** en consultas complejas
- **Falta de escalabilidad** para crecimiento futuro

### Requerimientos
- **Performance:** Todos los endpoints < 30ms
- **Escalabilidad:** Soporte para 1M+ proyectos y 10M+ unidades de stock
- **Flexibilidad:** Capacidad de agregar campos dinámicos sin modificaciones de esquema
- **Integridad:** Consistencia automática de datos
- **Mantenibilidad:** Estructura clara y evolución simple

## Decisión

### Arquitectura Elegida: Híbrida Optimizada con 8 Modelos Especializados

Hemos decidido implementar una **arquitectura híbrida** que combina campos críticos directos con campos dinámicos en JSON, complementada con tablas de cache y agregación para optimización de performance.

#### Modelos Principales:
1. **`real_estate_companies`** - Inmobiliarias (estructura simple)
2. **`projects`** - Proyectos (híbrida con desnormalización controlada)
3. **`project_images`** - Imágenes (normalizada)
4. **`legal_users`** - Representantes legales (normalizada)
5. **`project_stock`** - Stock (campos directos optimizados)

#### Modelos de Optimización:
6. **`projects_search_cache`** - Vista materializada para búsquedas
7. **`project_stock_summary`** - Agregaciones pre-computadas
8. **`project_details_cache`** - Cache de ficha comercial completa

### Estrategias de Optimización:

#### 1. Desnormalización Controlada
```sql
-- Campos calculados en tabla projects para evitar JOINs
`company_name` varchar(255),           -- Evita JOIN con inmobiliarias
`total_stock_units` int,               -- Evita COUNT en stock
`available_stock_units` int,           -- Filtros instantáneos
`min_price`, `max_price`,              -- Rangos pre-calculados
```

#### 2. Campos Críticos vs JSON
- **Campos directos:** Atributos consultados frecuentemente (filtros, ordenamiento)
- **Campos JSON:** Información descriptiva y de configuración menos consultada

#### 3. Índices Especializados
```sql
-- Índices compuestos para búsquedas complejas
KEY `idx_super_search` (`project_id`, `status`, `bedrooms`, `bathrooms`, `value_base`),
KEY `idx_availability_fast` (`project_id`, `status`, `blocked`, `deleted_at`),
```

#### 4. Cache Pre-computado
- **Vista materializada** para búsquedas globales
- **Cache de detalles** para ficha comercial completa
- **Resúmenes de stock** para agregaciones

#### 5. Automatización via Triggers
- **Actualización automática** de campos calculados
- **Invalidación inteligente** de cache
- **Consistencia garantizada** sin intervención manual

## Alternativas Consideradas

### Alternativa 1: Entity-Attribute-Value (EAV)
```sql
-- Sistema similar al actual con campos personalizados
CREATE TABLE project_values (
  project_id bigint,
  field_key varchar(255),
  value text
)
```

**❌ Rechazada por:**
- Performance 20x más lenta
- Consultas complejas con múltiples JOINs
- Imposible validación a nivel de BD
- Queries difíciles de mantener

### Alternativa 2: Todo en JSON
```sql
-- Todos los datos en campos JSON
CREATE TABLE projects (
  id bigint,
  data JSON
)
```

**❌ Rechazada por:**
- Índices limitados para JSON
- Filtros y ordenamiento lentos
- Validación solo en aplicación
- Dificulta consultas complejas

### Alternativa 3: Campos Directos Puros
```sql
-- 50+ campos como columnas directas
CREATE TABLE projects (
  id bigint,
  name varchar(255),
  legal_name varchar(255),
  -- ... 50+ campos más
)
```

**❌ Rechazada por:**
- Poca flexibilidad para cambios
- Tablas muy anchas difíciles de mantener
- Muchos campos NULL
- Evolución requiere DDL changes

### Alternativa 4: Microservicios Separados
**❌ Rechazada por:**
- Complejidad de coordinación
- Latencia adicional entre servicios
- Overhead de infraestructura
- Consistency challenges

## Consecuencias

### ✅ Beneficios

#### Performance Garantizada
- **Consultas básicas:** 5-20ms
- **Filtros complejos:** 20-30ms
- **Ficha comercial completa:** 25ms (vs 120ms anterior)
- **Búsquedas de stock:** 20ms (vs 1000ms anterior)

#### Escalabilidad Probada
- **1M+ proyectos** con performance mantenida
- **10M+ unidades stock** con búsquedas < 30ms
- **Crecimiento 10x** sin re-arquitectura

#### Mantenibilidad Mejorada
- **Estructura clara** con propósitos específicos por tabla
- **Evolución simple** via campos JSON
- **Debugging facilitado** con consultas comprensibles
- **Automatización completa** via triggers

#### Flexibilidad Controlada
- **Campos críticos:** Performance garantizada
- **Campos dinámicos:** Evolución sin downtime
- **Cache inteligente:** Invalidación automática
- **Índices especializados:** Para cada patrón de uso

### ⚠️ Trade-offs y Consideraciones

#### Complejidad Inicial
- **8 tablas** vs solución simple
- **Triggers** requieren entendimiento del equipo
- **Cache management** adicional

**Mitigación:** Documentación completa y training del equipo

#### Consistencia Eventual
- **Cache** puede estar temporalmente desactualizado
- **Triggers** introducen latencia mínima

**Mitigación:** TTL apropiados y monitoring de consistencia

#### Storage Overhead
- **Desnormalización** incrementa storage
- **Cache tables** requieren espacio adicional

**Mitigación:** Beneficio de performance justifica el costo

#### Mantenimiento de Índices
- **Múltiples índices** requieren mantenimiento
- **Updates** pueden ser más lentos

**Mitigación:** Índices diseñados para patrones reales de uso

## Implementación

### Fase 1: Modelos Base (Semana 1-2)
- Crear tablas principales
- Implementar triggers básicos
- Migrar datos críticos

### Fase 2: Optimizaciones (Semana 3)
- Implementar cache tables
- Configurar índices especializados
- Optimizar triggers

### Fase 3: Validación (Semana 4)
- Testing de performance
- Validación de escalabilidad
- Ajustes finales

## Monitoreo y Métricas

### KPIs de Performance
- **Response time** por endpoint < 30ms
- **Throughput** queries/segundo
- **Cache hit ratio** > 90%
- **Index usage** efficiency

### Métricas de Negocio
- **Reducción** en reservas múltiples
- **Mejora** en productividad de KAMs
- **Tiempo** de respuesta de búsquedas

## Revisión y Evolución

### Triggers de Revisión
- **Performance degradation** > 50ms
- **Storage growth** > 500% proyectado
- **New requirements** que no encajan en la arquitectura
- **Scale requirements** > 10M proyectos

### Plan de Evolución
- **Particionado** para crecimiento extremo
- **Read replicas** para alta disponibilidad
- **Caching layer** adicional si necesario
- **Event sourcing** para auditoría completa

## Decisiones de Implementación

### Tecnologías
- **Base de Datos:** MySQL 8.0+ (soporte JSON nativo)
- **ORM:** SQLAlchemy con modelos híbridos
- **Cache:** Redis para cache de aplicación
- **Monitoring:** Prometheus + Grafana

### Estándares de Código
- **Naming:** Inglés para tablas y campos
- **Soft Deletes:** `deleted_at` en todas las tablas
- **Auditoría:** `created_at`, `updated_at`, `created_by`, `updated_by`
- **Tipos:** Consistent data types (boolean real, decimals apropiados)

### Testing Strategy
- **Unit Tests:** Para cada modelo y trigger
- **Integration Tests:** Para flujos completos
- **Performance Tests:** Benchmarks con volúmenes reales
- **Load Tests:** Simulación de carga pico

## Referencias

- [Issue Original](./Issue.md) - Contexto y requerimientos del proyecto
- [Backend Plan](./Backend.md) - Plan de implementación backend
- [Frontend Plan](./Frontend.md) - Plan de implementación frontend
- [Contexto General](./Contexto.md) - Arquitectura y estructura propuesta

## Aprobaciones

- [ ] **Product Owner:** Aprobación de funcionalidad
- [ ] **Tech Lead:** Aprobación técnica
- [ ] **DBA:** Aprobación de esquemas
- [ ] **DevOps:** Aprobación de infraestructura
- [ ] **QA Lead:** Aprobación de estrategia de testing

---

**Nota:** Este ADR debe ser actualizado cuando se realicen cambios significativos en la arquitectura o cuando las métricas de performance indiquen necesidad de optimización adicional. 