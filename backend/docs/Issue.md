## 🔍 Contexto

El mantenedor de Proyectos y Stock es uno de nuestros mayores dolores en el equipo de ventas ya que no es fácil ni tampoco accesible actualizar estas entidades. **¿Por qué?** 🤔
- Para ambos casos, los Proyectos y el Stock se cargan por medio de una carpeta de Google Drive que tiene una determinada estructura, aquí se utiliza una de nuestras herramientas de Propital llamada **SyncStock**, que sincroniza tales archivos una X cantidad de veces durante el día.
- Para el caso puntual del Stock, el mayor dolor de las KAM es que las unidades aparecen desfasadas o no se actualizan en tiempo real, lo cual es un inconveniente dado que pueden haber casos como: reservas múltiples en una misma unidad.
- Esto produce que las KAMS (Key Account Manager / Ejecutivos de Negocio) vayan directamente al Google Drive y no utilicen nuestra fuente de la verdad llamada BackOffice, esto nos genera un problema porque necesitamos centralizar todo en un solo lugar para evitar cambios bruscos de contexto entre herramientas y para que toda la información quede relacionada entre sí.
- La ficha comercial debe estar orientada a mejorar la experiencia del Broker para que pueda asesorar de forma exitosa al cliente y concretar una reserva/venta.

## 🎯 Objetivo  

- Mejorar toda la interfaz de la ficha comercial y sus secciones/interacciones.
- Crear un sistema de gestión (AKA: mantenedor) tanto para los Proyectos como para el Stock, cabe aclarar que el Stock siempre y en cada uno de los casos va asociado a un proyecto ya creado.
- Esto contemplaría una implementación en AWS Lambdas (API) + Interfaz del Frontend para ejecutar las interacciones.
- Tener información accesible y centralizada para posteriormente utilizarlas en nuestras IA / Agentes.
- Evitar cambios de contextos bruscos entre Google Drive y nuestras plataformas.
- Eliminar todo AppServices.
- Eliminar el SyncStock.
- Una vez implementado, este sería el paso inicial para avanzar con Inmobiliarias B2B (Business to Business)
  - Inmobiliarias que pueden ingresar a BackOffice para ver el estado del Stock, Reservas y Negocios completados
  - API Pública de Proyectos/Stock (De esto se hablará en otra etapa del desarrollo)
- Una vez que se logre la implementación, cualquier persona del Staff podría modificar y actualizar esta información.
- Esta funcionalidad se lanzaría, en una primera instancia, a un grupo muy reducido de personas (versión beta) para que puedan hacer pruebas y una vez que se verifique el correcto funcionamiento, queda migrar las tablas viejas a la nueva versión.

## 📚 Alcance

- BackOffice
- AppServices (Ya no será necesario post implementación)
- SyncStock (Ya no será necesario post implementación)
- Propital Global (Apuntar a que se pueda reutilizar en otras plataformas)

## 📝 Accionables Backend

Crear una API que tengan los siguientes métodos inicialmente:

### Proyectos
- [ ] **GET All Projects**
  - Necesario para listar el nuevo Catálogo.
- [ ] **GET Project By Id**
  - Necesario para las fichas comerciales y lugares donde se utilicen los datos de un proyecto. 
- [ ] **POST Create Project**
  - Creación de un nuevo proyecto
  - Debería tener los siguientes campos:
  - Información General
    - Nombre `name`
    - Nombre legal `legal_name`
    - RUT `rut`
    - Empresa `company` | `supplier`
    - Fecha de entrega `delivery_date`
    - Fecha de término `delivery_end_date`
    - Fecha de lanzamiento comercial `launch_date`
    - Cuenta corriente (Inmobiliaria) `supplier_account`
    - Banco (Inmobiliaria) `supplier_bank`
    - Activo (Boolean) `active` por defecto: `false`
    - Consolidado `consolidated`
    - Ejecutivo `executive`
    - Descripción `description` (Considerar formato MarkDown)
  - Contacto y redes sociales
    - Teléfono `phone`
    - Sitio Web `website`
    - URL Tour Virtual `url_virtual_tour`
    - URL Facebook `url_facebook`
    - URL TikTok `url_tiktok`
    - URL Instagram `url_instagram`
    - URL Brochure `url_brochure`
  - Imágenes
    - Array de Strings con las url `images` [ '', '', '' ]
  - Ubicación
    - Dirección `address`
    - Región `city`
    - Comuna `state`
    - País `country`
    - Código postal `postal_code`
    - URL Google Maps `url_google_maps`
    - Latitud `latitude`
    - Longitud `longitude`
  - Arquitecto
    - Nombre `architect_first_name`
    - Apellido `architect_last_name`
    - Profesión `architect_profession`
    - RUT `architect_rut`
    - Correo `architect_email`
    - Teléfono `architect_phone`
    - Razón social `architect_social_reason`
    - Dirección `architect_address`
    - Comuna `architect_city`
  - Representantes Legales `legals` (Array múltiple)[ {}, {} ]
    - Nombre `first_name`
    - Apellido `last_name`
    - Profesión `profession`
    - RUT `rut`
    - Email `email`
    - Teléfono `phone`
    - Razón social `social_reason`
    - Dirección `address`
    - Comuna `city`
  - Finanzas
    - Reserva `reserve`
    - Empresa aseguradora `finances_insurance_company`
    - Monto poliza seguro `finances_insurance_policy`
    - Venta objetivo ponderado `finances_insured_value`
    - Venta objetivo útil `finances_insured_value_util`
    - Subsidio `finances_benefit`
    - Tasa anual `finances_annual_rate`
    - Tasa crédito hipotecario `finances_credit_rate`
    - *Averiguar cuales otros campos pueden servirnos aquí, o quitar los que no apliquen*
  - Stock
    - Aquí se insertarán las unidades luego haber creado el Proyecto, son 2 pasos.
    - Tiene que ser un array de objetos e inicialmente un array vacío.
- [ ] **PUT Update Project**
  - Modificación del proyecto.
  - Solo debe modificar aquellos valores que se le envíen en el body.
    - Es decir, si solo se envía el atributo `name`, debe dejar los demás intactos.
- [ ] **DELETE Delete Project**
  - Eliminar/suspender el proyecto.
  - Debería ser un soft delete sin eliminarlo de forma completa de la base de datos.

### Stock
- [ ] **GET Stock By ProjectId**
  - Necesario para las fichas comerciales y lugares donde se utilice el stock. 
- [ ] **POST Create Stock**
  - Creación de un nuevo stock asociado al id de un proyecto específico.
  - Debería tener los siguientes campos:
  - Información General
    - Proyecto `project_id`
    - Tipo `type`
    - Subtipo `subtype`
    - Nº Stock `number`
    - Descripción `description`
    - Descripción externa `external_description`
    - Estado `status`
    - Bloqueado `blocked` boolean
    - Compartido `shared` boolean
  - Atributos
    - Piso `floor`
    - Nº Piso `floor_number`
    - Orientación `orientation`
    - Etapa `stage`
    - Nº Dormitorios `bedrooms`
    - Nº Baños `bathrooms`
    - Nº Camas `beds`
    - Nº Estacionamientos `parking`
  - Superficies
    - Interior `surface_internal`
    - Terraza `surface_terrace`
    - Terraza Superior `surface_terrace_superior`
    - Jardín `surface_garden`
    - Jardín seco `surface_garden_dry`
    - Despensa `surface_pantry`
    - Sala multiusos asignable `surface_multiuse_assignable`
    - Ponderada `surface_ponderated`
    - Útil `surface_util`
    - Total `surface_total`
    - Interior municipal `surface_internal_municipal`
    - Terraza municipal `surface_terrace_municipal`
    - Total municipal `surface_municipal_total`
    - Mirador terraza `surface_terrace_mirador`
    - Terreno `surface_terrain` 
    - Otras superficies `surface_others`
  - Precios
    - Valor base `value_base`
    - Valor lista `value_list`
    - Valor lista original `value_list_original`
    - Valor venta `value_sale`
    - Valor venta base `value_sale_base`
    - Valor venta neta `value_sale_net`
    - Valor habilitación `value_enabled`
    - Valor promoción `value_promotion`
    - Valor bono `value_bonus`
    - Descuento autorizado `value_discount`
    - Descuento no autorizado `value_discount_unauthorized`
- [ ] **PUT Update Stock**
  - Modificación del proyecto.
  - Solo debe modificar aquellos valores que se le envíen en el body.
    - Es decir, si solo se envía el atributo `name`, debe dejar los demás intactos.
- [ ] **DELETE Delete Stock**
  - Eliminar/suspender el stock.
  - Debería ser un soft delete sin eliminarlo de forma completa de la base de datos.

## 📝 Accionables Frontend

### Proyectos
- [ ] Maquetado del módulo
- [ ] Integración completa con API
- [ ] Validaciones de entradas

### Stock
- [ ] Maquetado del módulo
- [ ] Integración completa API
- [ ] Validaciones de entradas

## 🔗 Recursos adicionales

- Los proyectos son aquellos que se listan en el Catálogo del BackOffice.
  - Ya existe un Catálogo hecho en una lambda, solo que quedará muy desactualizado ya que la nueva versión tendrá muchísimos campos nuevos, se sugiere crear una nueva versión desde 0.
- El Stock de un proyecto se puede visualizar en la Ficha Comercial de cada uno de ellos.
