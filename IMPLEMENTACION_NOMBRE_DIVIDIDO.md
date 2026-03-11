# Implementación: División del Nombre Completo

## Descripción General
Se ha implementado un sistema de división del campo "nombre_completo" en tres campos separados:
- **Apellido Paterno**: Campo obligatorio
- **Apellido Materno**: Campo opcional
- **Nombre(s)**: Campo obligatorio

El campo "nombre_completo" se genera automáticamente a partir de estos tres campos y no es visible para el usuario (está oculto).

---

## Cambios Realizados

### 1. **Modelo (portal/models.py)**
Se agregaron tres nuevos campos al modelo `PersonalEmpleados`:

```python
apellido_paterno = models.CharField(max_length=100, help_text='Apellido paterno del empleado')
apellido_materno = models.CharField(max_length=100, blank=True, help_text='Apellido materno del empleado')
nombre = models.CharField(max_length=100, help_text='Nombre(s) del empleado')
nombre_completo = models.CharField(max_length=200, editable=False, help_text='Se genera automáticamente')
```

El método `save()` fue modificado para generar automáticamente el `nombre_completo`:
```python
def save(self, *args, **kwargs):
    """Generar nombre_completo automáticamente"""
    if self.apellido_materno:
        self.nombre_completo = f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    else:
        self.nombre_completo = f"{self.nombre} {self.apellido_paterno}"
    super().save(*args, **kwargs)
```

### 2. **Migraciones (portal/migrations/)**

**Migración 0014**: `0014_personalempleados_nombre_dividido.py`
- Agrega los tres nuevos campos
- Modifica `nombre_completo` para que sea `editable=False`

**Migración 0015**: `0015_alter_personalpuestos_options_and_more.py`
- Actualiza las opciones de Meta en los modelos

### 3. **Formulario (portal/forms.py)**
Actualizado `PersonalEmpleadosForm` con:
- Los tres nuevos campos en la lista `fields`
- Widgets Bootstrap para cada campo
- Labels en español
- Validaciones apropiadas

```python
fields = [
    'usuario',
    'email',
    'apellido_paterno',    # NUEVO
    'apellido_materno',    # NUEVO
    'nombre',              # NUEVO
    # ... resto de campos
]
```

### 4. **Templates (HTML)**

#### crear_empleado.html
Actualizado para:
- Mostrar tres campos de entrada para los nombres (dividido en dos filas)
- Ocultar el campo `nombre_completo` con `{{ form.nombre_completo }}`
- Mostrar una vista previa del nombre completo en un alert box
- Incluir JavaScript para actualizar la vista previa en tiempo real

Sección Identificación ahora muestra:
```html
<!-- Campos de Nombre Dividido -->
<div class="row">
    <div class="col-md-6 mb-3">
        <label for="{{ form.apellido_paterno.id_for_label }}" class="form-label fw-bold">
            {{ form.apellido_paterno.label }} <span class="text-danger">*</span>
        </label>
        {{ form.apellido_paterno }}
    </div>
    <div class="col-md-6 mb-3">
        <label for="{{ form.apellido_materno.id_for_label }}" class="form-label fw-bold">
            {{ form.apellido_materno.label }}
        </label>
        {{ form.apellido_materno }}
    </div>
</div>
<div class="mb-3">
    <label for="{{ form.nombre.id_for_label }}" class="form-label fw-bold">
        {{ form.nombre.label }} <span class="text-danger">*</span>
    </label>
    {{ form.nombre }}
</div>

<!-- Vista previa del nombre completo -->
<div class="alert alert-info" role="alert">
    <small><strong>Nombre Completo (generado automáticamente):</strong></small>
    <div id="nombre-completo-preview" class="mt-2" style="font-size: 1.1em; font-weight: 600;">
        (se generará automáticamente)
    </div>
</div>
```

#### editar_empleado.html
Actualizado con la misma estructura que `crear_empleado.html` para mantener consistencia.

#### ver_empleado.html
Ya mostraba el `nombre_completo` correctamente, sin cambios necesarios.

### 5. **JavaScript**

#### portal/static/desarrollo/js/nombre-completo.js
Nuevo archivo que:
- Detecta cambios en los campos `apellido_paterno`, `apellido_materno` y `nombre`
- Genera el nombre completo en tiempo real
- Actualiza la vista previa en el elemento `#nombre-completo-preview`
- Se ejecuta al cargar la página y cada vez que se modifica un campo

Características:
- Limpia espacios en blanco
- Valida que existan los elementos necesarios
- Funciona tanto en creación como en edición
- Compatible con todos los navegadores modernos

#### portal/static/desarrollo/js/departamentos-cascada.js
Script existente que continúa funcionando:
- Carga departamentos según la dirección seleccionada
- Preserva valores al editar
- Consulta via AJAX el endpoint `/api/departamentos-por-direccion/`

### 6. **Admin (portal/admin.py)**
Actualizado `PersonalEmpleadosAdmin` para mostrar los nuevos campos en el panel de administración.

---

## Comportamiento del Sistema

### Creación de Empleado
1. Usuario ingresa: Apellido Paterno, Apellido Materno (opcional), Nombre(s)
2. JavaScript valida en tiempo real y muestra vista previa del nombre completo
3. Al guardar, Django genera automáticamente `nombre_completo` en la base de datos
4. El empleado aparece en listados con el nombre completo

### Edición de Empleado
1. Los campos se cargan con los valores existentes
2. JavaScript muestra la vista previa al cargar la página
3. Los cambios se reflejan en la vista previa
4. Al guardar, `nombre_completo` se actualiza automáticamente

### Visualización
- En listas de empleados: Se muestra el `nombre_completo`
- En vista detallada: Se muestra el `nombre_completo` junto con otros datos

---

## Requisitos Cumplidos

✅ **Nombre dividido en tres campos**
- Apellido Paterno (obligatorio)
- Apellido Materno (opcional)
- Nombre(s) (obligatorio)

✅ **Generación automática de nombre completo**
- Se calcula en la capa de modelo (método `save()`)
- Se calcula en la capa de formulario (JavaScript)
- No visible para el usuario (campo oculto)

✅ **Vista previa en tiempo real**
- Se actualiza mientras el usuario escribe
- Muestra exactamente cómo aparecerá en la base de datos

✅ **Compatibilidad con funciones existentes**
- Cascada de Dirección → Departamento sigue funcionando
- Carga de Puestos sigue funcionando
- Carga de Tipos de Contratación sigue funcionando
- Todas las demás funcionalidades se mantienen intactas

---

## Archivos Modificados

| Archivo | Cambios |
|---------|---------|
| `portal/models.py` | Agregados 3 campos + método save() modificado |
| `portal/forms.py` | Actualizados campos del formulario |
| `portal/migrations/0014_*.py` | NUEVA migración para agregar campos |
| `portal/migrations/0015_*.py` | NUEVA migración para opciones de Meta |
| `portal/templates/desarrollo/empleados/crear_empleado.html` | Sección de Identificación actualizada |
| `portal/templates/desarrollo/empleados/editar_empleado.html` | Sección de Identificación actualizada |
| `portal/static/desarrollo/js/nombre-completo.js` | NUEVO archivo JavaScript |

---

## Pruebas Realizadas

✅ `manage.py check` - Sin errores
✅ `manage.py makemigrations` - Migraciones generadas correctamente
✅ `manage.py migrate` - Migraciones aplicadas sin errores
✅ Formulario de creación - Funciona correctamente
✅ Formulario de edición - Funciona correctamente
✅ Vista previa de nombre - Se actualiza en tiempo real
✅ Cascada Dirección → Departamento - Funciona correctamente
✅ Admin de Django - Muestra los nuevos campos

---

## Instrucciones de Deployment

1. **Aplicar migraciones**:
   ```bash
   python manage.py migrate
   ```

2. **Recolectar archivos estáticos** (si está en producción):
   ```bash
   python manage.py collectstatic
   ```

3. **Reiniciar el servidor** Django

4. **Verificar**:
   - Crear un nuevo empleado
   - Editar un empleado existente
   - Verificar que el nombre completo se genera correctamente

---

## Notas Técnicas

- La generación de `nombre_completo` ocurre en el nivel de modelo (más confiable)
- JavaScript proporciona vista previa sin guardar
- El campo `nombre_completo` es `editable=False` para evitar manipulación directa
- Apellido Materno es opcional (`blank=True`)
- Apellido Paterno y Nombre son obligatorios
- Compatible con búsquedas y ordenamiento por `nombre_completo`

---

## Cambios Futuros Potenciales

- Agregar validación de CURP basada en nombres
- Agregar generador automático de RFC
- Permitir búsqueda por componentes del nombre
- Agregar historial de cambios de nombre (auditoría)


