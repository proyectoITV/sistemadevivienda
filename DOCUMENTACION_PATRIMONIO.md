# Módulo de Patrimonio - ITAVU

## Descripción

El módulo de **Patrimonio** ha sido implementado para gestionar el inventario de bienes del Instituto. Este módulo permite registrar, actualizar y dar seguimiento a todos los artículos de patrimonio con información detallada técnica, de compra y clasificación.

## Estructura del Módulo

### Ubicación en el menú
- **Dirección de Administración** → **Recursos Humanos** → **Patrimonio** → **Bienes del Instituto**

### URL Principal
```
http://127.0.0.1:8000/patrimonio/bienes/
```

## Modelos Implementados

### 1. **CatalogosMarcas**
- **Tabla**: `catalogos_marcas`
- **Propósito**: Almacenar marcas de artículos
- **Campos**: idmarca, nombre, descripción, activo
- **Datos precargados**: HP, Dell, Lenovo, Asus, Apple, Canon, Epson, Samsung, LG, Xerox, Office Depot, Steelcase

### 2. **PatrimonioClasificacionSerap**
- **Tabla**: `patrimonio_clasificacionserap`
- **Propósito**: Clasificar bienes según SERAP (Secretaría de la Función Pública)
- **Clasificaciones precargadas**:
  - Equipo de comunicación
  - Equipo de computo
  - Herramienta
  - Mobiliario y equipo de oficina

### 3. **PatrimonioClasificacionContraloria**
- **Tabla**: `patrimonio_clasificacioncontraloria`
- **Propósito**: Clasificar bienes según Contraloría
- **Clasificaciones precargadas**:
  - Bien controlable
  - Bien controlable - gasto
  - Bien inventariable
  - Bienes baja definitiva

### 4. **PatrimonioProveedor**
- **Tabla**: `patrimonio_proveedor`
- **Propósito**: Gestionar información de proveedores
- **Campos**: idproveedor, nombre, RFC, teléfono, correo, domicilio, persona_contacto
- **Proveedores precargados**: Ingram Micro, Softland, Grupo Econom, Muebles Corporativos

### 5. **PatrimonioBienesDelInstituto**
- **Tabla**: `patrimonio_bienes_del_instituto`
- **Propósito**: Registro principal de bienes
- **Campos principales**:

#### Identificación:
- `numero_inventario_itavu` - Número único ITAVU (requerido)
- `numero_inventario_gobierno` - Número de gobierno (opcional)
- `descripcion` - Descripción del bien (requerido)
- `fotografia` - Foto del bien (opcional)

#### Especificaciones técnicas:
- `marca` - FK a CatalogosMarcas
- `modelo` - Modelo del bien
- `serie` - Número de serie único

#### Información de compra:
- `fecha_factura` - Fecha de facturación
- `numero_factura` - Número de factura (único)
- `costo_articulo` - Costo en moneda (requerido)
- `proveedor` - FK a PatrimonioProveedor

#### Clasificaciones:
- `clasificacion_serap` - FK a PatrimonioClasificacionSerap
- `clasificacion_contraloria` - FK a PatrimonioClasificacionContraloria

#### Información adicional:
- `observaciones` - Notas sobre el bien
- `activo` - Estado del bien en inventario
- `usuario_captura` - Usuario que registró
- `usuario_modificacion` - Usuario que modificó

## Funcionalidades

### 1. Listar Bienes
- **URL**: `/patrimonio/bienes/`
- **Método**: GET
- **Descripción**: Muestra tabla paginada de todos los bienes
- **Características**:
  - Búsqueda por: número inventario ITAVU, número gobierno, descripción, serie, factura
  - Filtrado por estado (Activo/Inactivo)
  - Tabla con información resumida
  - Botones de acción: Editar, Cambiar estado

### 2. Crear Bien
- **URL**: `/patrimonio/bienes/crear/`
- **Método**: POST
- **Descripción**: Formulario para registrar nuevo bien
- **Campos**: Todos excepto fecha_registro (se genera automáticamente)
- **Validaciones**: 
  - Número inventario ITAVU debe ser único
  - Número de serie debe ser único (si se proporciona)
  - Número de factura debe ser único (si se proporciona)
  - Costo debe ser numérico positivo

### 3. Editar Bien
- **URL**: `/patrimonio/bienes/<idbien>/editar/`
- **Método**: POST
- **Descripción**: Actualizar información del bien
- **Restricciones**: No se puede cambiar el número de inventario ITAVU

### 4. Cambiar Estado Bien
- **URL**: `/patrimonio/bienes/<idbien>/estado/`
- **Método**: GET/POST
- **Descripción**: Cambiar estado entre Activo e Inactivo
- **Efecto**: Invierte el estado actual del bien

## Campos del Formulario

### Información Básica
```
Número Inventario ITAVU*     | Texto (50 caracteres máximo)
Número Inventario Gobierno   | Texto (50 caracteres máximo)
Descripción*                 | Texto (255 caracteres máximo)
Fotografía                   | Archivo de imagen
```

### Especificaciones Técnicas
```
Marca                        | Selección (FK CatalogosMarcas)
Modelo                       | Texto (100 caracteres)
Número de Serie              | Texto (100 caracteres, único)
```

### Información de Compra
```
Fecha de Factura             | Fecha (DD/MM/YYYY)
Número de Factura            | Texto (50 caracteres, único)
Costo del Artículo*          | Decimal (12 dígitos, 2 decimales)
Proveedor                    | Selección (FK PatrimonioProveedor)
```

### Clasificaciones
```
Clasificación SERAP          | Selección (FK PatrimonioClasificacionSerap)
Clasificación Contraloría    | Selección (FK PatrimonioClasificacionContraloria)
```

### Información Adicional
```
Observaciones                | Textarea
Activo                       | Checkbox
```

## Permisos

- **Ver/Listar**: Todos los usuarios autenticados
- **Crear**: Todos los usuarios autenticados
- **Editar**: Todos los usuarios autenticados
- **Cambiar Estado**: Todos los usuarios autenticados

*Nota: Se recomienda restricción posterior por roles*

## Script de Carga Inicial

Se incluye el archivo `cargar_patrimonio.py` que precarga:
- 12 marcas comunes
- 4 clasificaciones SERAP
- 4 clasificaciones de Contraloría
- 4 proveedores de ejemplo

**Ejecutar**:
```bash
python cargar_patrimonio.py
```

## Rutas (URLs) del módulo

```python
# Listar
/patrimonio/bienes/                    → listar_bienes (name: 'listar_bienes')

# Crear
/patrimonio/bienes/crear/              → crear_bien (name: 'crear_bien')

# Editar
/patrimonio/bienes/<idbien>/editar/    → editar_bien (name: 'editar_bien')

# Cambiar estado
/patrimonio/bienes/<idbien>/estado/    → cambiar_estado_bien (name: 'cambiar_estado_bien')
```

## Índices de Base de Datos

Se han creado índices en los campos frecuentemente consultados:
- `numero_inventario_itavu`
- `numero_inventario_gobierno`
- `activo`

## Observaciones

1. **Fotografías**: Se almacenan en `/media/patrimonio/fotos/`
2. **Auditoría**: Se registran usuario_captura y usuario_modificacion
3. **Timestamps**: fecha_creacion y fecha_modificacion se generan automáticamente
4. **Búsqueda**: Case-insensitive en todos los campos de búsqueda
5. **Estados**: Un bien puede estar Activo (en uso) o Inactivo (retirado, extraviado, etc.)

## Próximas Mejoras Sugeridas

- [ ] Importar/Exportar bienes (Excel, CSV)
- [ ] Generar reportes de patrimonio
- [ ] Historial de cambios y movimientos de bienes
- [ ] Depreciación y valor actual
- [ ] Asignación de bienes a empleados/departamentos
- [ ] Códigos QR/Códigos de barras
- [ ] Control de cambios de ubicación
- [ ] Alertas por vencimiento de garantía
- [ ] Integración con fotografía automática
- [ ] Sincronización con sistemas de compras

## Soporte

Para reportar problemas o sugerencias sobre el módulo de Patrimonio, contactar con el equipo de desarrollo.
