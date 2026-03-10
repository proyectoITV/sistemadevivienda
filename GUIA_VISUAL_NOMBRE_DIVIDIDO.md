# Guía Visual: División del Nombre Completo

## Flujo de Usuario - Creación de Empleado

### Antes (Sistema Anterior)
```
┌─────────────────────────────────────────────────────────────┐
│ FORMULARIO DE CREACIÓN DE EMPLEADO (VERSIÓN ANTERIOR)      │
├─────────────────────────────────────────────────────────────┤
│ Identificación                                              │
│                                                             │
│ Usuario: [________________]  Email: [________________]      │
│                                                             │
│ Fotografía: [Seleccionar archivo]                          │
│                                                             │
│ Nombre Completo: [_________________________________]       │
│                                                             │
│ Contraseña: [________________]                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Problemas:**
- Un solo campo para todo el nombre
- Difícil de validar componentes
- Error del usuario genera nombre mal formado
- Imposible generar CURP o RFC automáticamente

---

### Después (Sistema Mejorado)
```
┌─────────────────────────────────────────────────────────────┐
│ FORMULARIO DE CREACIÓN DE EMPLEADO (VERSIÓN MEJORADA)      │
├─────────────────────────────────────────────────────────────┤
│ Identificación                                              │
│                                                             │
│ Usuario: [________________]  Email: [________________]      │
│          Fotografía: [Seleccionar archivo]                 │
│                                                             │
│ Apellido Paterno*: [________________]                       │
│ Apellido Materno: [_____________]                          │
│ Nombre(s)*: [________________]                              │
│                                                             │
│ ℹ️ Nombre Completo (generado automáticamente):             │
│    Juan García López                                        │
│                                                             │
│ Contraseña*: [________________]                             │
│                                                             │
│                      [CREAR]  [CANCELAR]                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Mejoras:**
✅ Campos separados para mayor claridad
✅ Validación independiente por componente
✅ Vista previa en tiempo real
✅ Nombre completo correcto garantizado
✅ Compatible con generadores de CURP/RFC

---

## Secuencia de Interacción - Creación

### Paso 1: Usuario ingresa Apellido Paterno
```
Apellido Paterno*: [García________]
Apellido Materno:  [______________]
Nombre(s)*:        [______________]

ℹ️ Nombre Completo (generado automáticamente):
   (se generará automáticamente)
```

### Paso 2: Usuario ingresa Apellido Materno
```
Apellido Paterno*: [García________]
Apellido Materno:  [López_________]
Nombre(s)*:        [______________]

ℹ️ Nombre Completo (generado automáticamente):
   (se generará automáticamente)
```

### Paso 3: Usuario ingresa Nombre(s)
```
Apellido Paterno*: [García________]
Apellido Materno:  [López_________]
Nombre(s)*:        [Juan__________]

ℹ️ Nombre Completo (generado automáticamente):
   Juan García López
```
*La vista previa se actualiza automáticamente*

### Paso 4: Usuario envía el formulario
Base de datos registra:
- `apellido_paterno`: "García"
- `apellido_materno`: "López"
- `nombre`: "Juan"
- `nombre_completo`: "Juan García López" (generado automáticamente)

---

## Flujo de Usuario - Edición de Empleado

### Abriendo formulario de edición
```
┌─────────────────────────────────────────────────────────────┐
│ FORMULARIO DE EDICIÓN DE EMPLEADO                           │
├─────────────────────────────────────────────────────────────┤
│ Identificación                                              │
│                                                             │
│ Usuario: [jgarcia________]  Email: [jgarcia@empresa.com]   │
│          Fotografía: [Cambiar] [Ver actual]                │
│                                                             │
│ Apellido Paterno*: [García________] (pre-cargado)          │
│ Apellido Materno: [López_________]  (pre-cargado)          │
│ Nombre(s)*:        [Juan__________] (pre-cargado)          │
│                                                             │
│ ℹ️ Nombre Completo (generado automáticamente):             │
│    Juan García López                                        │
│                                                             │
│ Contraseña*: [________________] (deixar en blanco si no...│
│                                                             │
│                      [GUARDAR]  [CANCELAR]                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Usuario modifica el nombre
Usuario cambió "López" a "Martínez":

```
Apellido Paterno*: [García________]
Apellido Materno: [Martínez_______]  ← modificado
Nombre(s)*:        [Juan__________]

ℹ️ Nombre Completo (generado automáticamente):
   Juan García Martínez  ← actualizado en tiempo real
```

---

## Validaciones Implementadas

### En el modelo (Backend)
```python
✅ apellido_paterno: obligatorio, máx 100 caracteres
✅ apellido_materno: opcional, máx 100 caracteres
✅ nombre: obligatorio, máx 100 caracteres
✅ nombre_completo: generado automáticamente, no editable
```

### En el formulario (Frontend)
```python
✅ Campos validados por Django
✅ Widgets con clases Bootstrap
✅ Labels en español
✅ Placeholders descriptivos
✅ Mensajes de error claros
```

### En JavaScript (Interactividad)
```javascript
✅ Validación de existencia de elementos
✅ Trim de espacios en blanco
✅ Actualización en tiempo real
✅ Fallback si JavaScript está deshabilitado
```

---

## Listado de Empleados

### Vista anterior (solo nombre_completo)
```
┌──────┬──────────────────────┬─────────────┬─────────────┐
│ ID   │ Nombre Completo      │ Puesto      │ Acciones    │
├──────┼──────────────────────┼─────────────┼─────────────┤
│ 1    │ Juan García López    │ Gerente     │ [Ver][Edit] │
│ 2    │ María Rodríguez      │ Empleado    │ [Ver][Edit] │
│ 3    │ Carlos López Martín  │ Supervisor  │ [Ver][Edit] │
└──────┴──────────────────────┴─────────────┴─────────────┘
```

---

## Integración con Otros Sistemas

### Cascada Dirección → Departamento
Continúa funcionando normalmente:
```javascript
- JavaScript en departamentos-cascada.js
- AJAX endpoint: /api/departamentos-por-direccion/
- Carga dinámicamente los departamentos según dirección
```

### Tipos de Contratación
Continúa funcionando normalmente:
```
- 3 tipos: Sindical, Extraordinario, Operativo
- Cargados desde base de datos
- Validados al guardar empleado
```

### Puestos
Continúa funcionando normalmente:
```
- 31 puestos disponibles
- Cargados desde base de datos
- Validados al guardar empleado
```

---

## Flujo de Datos Completo

```
┌─────────────────────────────────────────────────────────────┐
│ USUARIO INGRESA DATOS EN FORMULARIO HTML                   │
├─────────────────────────────────────────────────────────────┤
│ ├─ Apellido Paterno: García                                 │
│ ├─ Apellido Materno: López                                  │
│ └─ Nombre(s): Juan                                          │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ JAVASCRIPT ACTUALIZA VISTA PREVIA (tiempo real)            │
├─────────────────────────────────────────────────────────────┤
│ → Ejecuta nombre-completo.js                                │
│ → Muestra: "Juan García López" en preview                   │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ USUARIO ENVÍA FORMULARIO (POST)                             │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ DJANGO PROCESA FORMULARIO                                   │
├─────────────────────────────────────────────────────────────┤
│ → PersonalEmpleadosForm valida datos                        │
│ → Crea instancia PersonalEmpleados                          │
│ → Llama al método save()                                    │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ MODELO save() GENERA NOMBRE_COMPLETO                        │
├─────────────────────────────────────────────────────────────┤
│ if self.apellido_materno:                                   │
│     nombre_completo = "Juan García López"                   │
│ else:                                                       │
│     nombre_completo = "Juan García"                         │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ GUARDA EN BASE DE DATOS                                     │
├─────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────┐                        │
│ │ personal_empleados               │                        │
│ ├──────────────────────────────────┤                        │
│ │ id_empleado: 1                   │                        │
│ │ usuario: jgarcia                 │                        │
│ │ email: jgarcia@empresa.com       │                        │
│ │ apellido_paterno: García         │ ← Separado            │
│ │ apellido_materno: López          │ ← Separado            │
│ │ nombre: Juan                     │ ← Separado            │
│ │ nombre_completo: Juan García López │ ← Generado            │
│ │ ...                              │                        │
│ └──────────────────────────────────┘                        │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│ USUARIO VE CONFIRMACIÓN                                     │
├─────────────────────────────────────────────────────────────┤
│ ✓ Empleado creado correctamente                             │
│                                                             │
│ Nombre: Juan García López                                   │
│ Usuario: jgarcia                                            │
│ Email: jgarcia@empresa.com                                  │
│ Puesto: Gerente                                             │
│ Departamento: Dirección Comercial                           │
│                                                             │
│                      [VOLVER A EMPLEADOS]                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Beneficios de la Implementación

| Aspecto | Antes | Después |
|--------|-------|---------|
| **Validación** | Manual, propensa a errores | Automática y confiable |
| **Claridad** | 1 campo ambiguo | 3 campos específicos |
| **Prevención de errores** | Usuario puede escribir cualquier cosa | Orden predecible: Apellido Paterno + Apellido Materno + Nombre |
| **Compatibilidad CURP** | No es posible generar | Ahora es posible (futuro) |
| **Compatibilidad RFC** | No es posible generar | Ahora es posible (futuro) |
| **Búsquedas** | Por nombre completo | Potencialmente por componente (futuro) |
| **UX** | Confuso | Clara y intuitiva |
| **Consistencia** | Variable | 100% consistente |

---

## Ejemplo de Datos Guardados

### Antes
```json
{
  "id_empleado": 1,
  "usuario": "jgarcia",
  "email": "jgarcia@empresa.com",
  "nombre_completo": "juan garcia lopez",
  "puesto": "Gerente",
  "departamento": "Comercial"
}
```
*Inconsistente: minúsculas, espacios variables, imposible separar*

### Después
```json
{
  "id_empleado": 1,
  "usuario": "jgarcia",
  "email": "jgarcia@empresa.com",
  "apellido_paterno": "García",
  "apellido_materno": "López",
  "nombre": "Juan",
  "nombre_completo": "Juan García López",
  "idpuesto": 5,
  "puesto": "Gerente",
  "iddepartamento": 3,
  "departamento": "Dirección Comercial"
}
```
*Consistente: componentes separados, nombre completo generado, sin errores*

---

## Resumen

La implementación de división del nombre completo en tres campos separados:

✅ **Mejora la calidad de datos**: Cada componente es validado por separado
✅ **Simplifica la interfaz**: Campos claros y específicos
✅ **Aumenta la automatización**: Nombre completo se genera automáticamente
✅ **Prepara el futuro**: Permite generación de CURP/RFC automática
✅ **Mantiene compatibilidad**: Todos los sistemas existentes continúan funcionando
✅ **Mejora UX**: Vista previa en tiempo real
✅ **Garantiza consistencia**: Datos predecibles en base de datos

