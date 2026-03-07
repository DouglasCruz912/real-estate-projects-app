# Plan de Acción Backend - API Proyectos y Stock

## Tareas de Desarrollo (En orden de prioridad)

### 1. Preparación de Infraestructura
1. **Configurar estructura base FastAPI** - Crear arquitectura de carpetas escalable
2. **Configurar conexión a MySQL** - Setup de modelos SQLAlchemy y configuración DB
3. **Implementar autenticación y middleware** - Sistema de permisos para administradores

### 2. Gestión de Proyectos
4. **Reorganizar relaciones de tablas** - Analizar tablas existentes y crear modelos compatibles
5. **Implementar POST /projects** - Crear proyecto con campos mínimos requeridos
6. **Implementar GET /projects** - Listar todos los proyectos con paginación
7. **Implementar GET /projects/{id}** - Obtener proyecto específico
8. **Implementar PUT /projects/{id}** - Actualizar información del proyecto
9. **Implementar DELETE /projects/{id}** - Soft delete del proyecto

### 3. Gestión de Stock
10. **Implementar POST /projects/{id}/stock** - Crear stock asociado a proyecto
11. **Implementar GET /projects/{id}/stock** - Listar stock de un proyecto
12. **Implementar PUT /stock/{id}** - Actualizar unidad de stock
13. **Implementar DELETE /stock/{id}** - Soft delete de unidad de stock

### 4. Endpoints Especializados
14. **Implementar GET /projects/{id}/details** - Ficha comercial completa (proyecto + stock)
15. **Implementar filtros y búsquedas** - Query parameters para filtrado avanzado
16. **Implementar validaciones de negocio** - Reglas específicas del dominio

### 5. Optimización y Testing
17. **Implementar tests unitarios** - Cobertura de endpoints críticos
18. **Optimizar consultas SQL** - Performance y relaciones eficientes
19. **Documentación API** - Swagger/OpenAPI completo
20. **Deploy y monitoring** - Configuración AWS Lambda y logs
