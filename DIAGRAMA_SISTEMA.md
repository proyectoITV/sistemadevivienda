# 📊 Diagrama del Sistema - División del Nombre Completo

## Arquitectura General

```
┌────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE GESTIÓN DE EMPLEADOS                 │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────────────┐                                         │
│  │   BASE DE DATOS      │                                         │
│  │  (MySQL/MariaDB)     │                                         │
│  ├──────────────────────┤                                         │
│  │ personal_empleados   │                                         │
│  │ ├─ id_empleado       │                                         │
│  │ ├─ usuario ⭐        │ ← PK                                     │
│  │ ├─ email             │                                         │
│  │ ├─ apellido_paterno  │ ← NUEVO                                 │
│  │ ├─ apellido_materno  │ ← NUEVO (opcional)                      │
│  │ ├─ nombre            │ ← NUEVO                                 │
│  │ ├─ nombre_completo   │ ← AUTOGENERADO                          │
│  │ ├─ iddepartamento    │ ← FK                                    │
│  │ ├─ idpuesto          │ ← FK                                    │
│  │ ├─ idtipodecontratacion │ ← FK                                 │
│  │ ├─ fotografia        │                                         │
│  │ └─ ... otros campos  │                                         │
│  └────────┬─────────────┘                                         │
│           │                                                        │
│           │ ORM                                                    │
│           ↓                                                        │
│  ┌────────────────────────────────────────────────────┐           │
│  │        Django ORM (models.py)                      │           │
│  │                                                    │           │
│  │  PersonalEmpleados                                │           │
│  │  ├─ Campos de nombre (3)                          │           │
│  │  └─ save() → Genera nombre_completo              │           │
│  └────────┬──────────────────────────────────────────┘           │
│           │                                                        │
│           │ Validación                                            │
│           ↓                                                        │
│  ┌────────────────────────────────────────────────────┐           │
│  │      Django Forms (forms.py)                       │           │
│  │                                                    │           │
│  │  PersonalEmpleadosForm                            │           │
│  │  ├─ apellido_paterno (obligatorio)               │           │
│  │  ├─ apellido_materno (opcional)                  │           │
│  │  ├─ nombre (obligatorio)                         │           │
│  │  ├─ Widgets Bootstrap                            │           │
│  │  └─ Validaciones en server                       │           │
│  └────────┬──────────────────────────────────────────┘           │
│           │                                                        │
│           │ URLs / Vistas                                         │
│           ↓                                                        │
│  ┌────────────────────────────────────────────────────┐           │
│  │      Django Views (views.py)                       │           │
│  │                                                    │           │
│  │  crear_empleado(request)                          │           │
│  │  editar_empleado(request, id)                     │           │
│  │  ver_empleado(request, id)                        │           │
│  │  listar_empleados(request)                        │           │
│  │  get_departamentos_por_direccion() [AJAX]        │           │
│  └────────┬──────────────────────────────────────────┘           │
│           │                                                        │
│           │ Renderizado                                           │
│           ↓                                                        │
│  ┌────────────────────────────────────────────────────┐           │
│  │      Templates HTML (templates/)                  │           │
│  │                                                    │           │
│  │  ├─ crear_empleado.html                           │           │
│  │  │  ├─ Form con 3 campos de nombre               │           │
│  │  │  ├─ Vista previa en alert box                 │           │
│  │  │  └─ Scripts JS incluidos                       │           │
│  │  │                                                │           │
│  │  ├─ editar_empleado.html                          │           │
│  │  │  ├─ Form pre-cargado                          │           │
│  │  │  ├─ Vista previa actualizada                  │           │
│  │  │  └─ Scripts JS incluidos                       │           │
│  │  │                                                │           │
│  │  └─ ver_empleado.html                             │           │
│  │     └─ Muestra nombre_completo                    │           │
│  └────────┬──────────────────────────────────────────┘           │
│           │                                                        │
│           │ JavaScript Interactividad                             │
│           ↓                                                        │
│  ┌────────────────────────────────────────────────────┐           │
│  │      JavaScript (static/js/)                      │           │
│  │                                                    │           │
│  │  nombre-completo.js                               │           │
│  │  ├─ Detecta cambios en campos de nombre          │           │
│  │  ├─ Actualiza preview en tiempo real             │           │
│  │  ├─ 'change' + 'keyup' listeners                 │           │
│  │  └─ DOMContentLoaded inicialización              │           │
│  │                                                    │           │
│  │  departamentos-cascada.js                         │           │
│  │  ├─ Carga departamentos por dirección (AJAX)     │           │
│  │  └─ Preserva valores en edición                  │           │
│  └────────┬──────────────────────────────────────────┘           │
│           │                                                        │
│           │ HTTP Requests/Responses                               │
│           ↓                                                        │
│  ┌────────────────────────────────────────────────────┐           │
│  │      Navegador del Usuario                        │           │
│  │                                                    │           │
│  │  ✅ Interfaz responsive                           │           │
│  │  ✅ Bootstrap 5 styling                           │           │
│  │  ✅ Live preview de nombre                        │           │
│  │  ✅ Validación cliente                            │           │
│  │  ✅ Compatible con todos los navegadores         │           │
│  └────────────────────────────────────────────────────┘           │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Creación de Empleado

```
START
  │
  ├─ Usuario accede a /empleados/crear/
  │
  ├─ Servidor renderiza crear_empleado.html
  │  │
  │  └─ Incluye: nombre-completo.js + departamentos-cascada.js
  │
  ├─ Navegador carga página con formulario
  │  │
  │  ├─ Campo: Apellido Paterno [________]
  │  ├─ Campo: Apellido Materno [________]
  │  ├─ Campo: Nombre(s) [________]
  │  └─ Preview: (se generará automáticamente)
  │
  ├─ Usuario escribe: "García" en Apellido Paterno
  │  │
  │  └─ nombre-completo.js detecta evento 'keyup'
  │     └─ Preview: "(se generará automáticamente)" [sin cambio aún]
  │
  ├─ Usuario escribe: "López" en Apellido Materno
  │  │
  │  └─ nombre-completo.js detecta evento 'keyup'
  │     └─ Preview: "(se generará automáticamente)" [sin cambio aún]
  │
  ├─ Usuario escribe: "Juan" en Nombre(s)
  │  │
  │  └─ nombre-completo.js detecta evento 'keyup'
  │     └─ Preview: "Juan García López" ✅ ACTUALIZADO
  │
  ├─ Usuario hace clic en [CREAR]
  │  │
  │  └─ Formulario se envía (POST)
  │
  ├─ Django recibe POST en crear_empleado
  │  │
  │  ├─ PersonalEmpleadosForm valida datos
  │  │  ├─ apellido_paterno: "García" ✅
  │  │  ├─ apellido_materno: "López" ✅
  │  │  ├─ nombre: "Juan" ✅
  │  │  └─ Otros campos... ✅
  │  │
  │  └─ Form es válido
  │
  ├─ Crea instancia PersonalEmpleados
  │
  ├─ Llama a .save()
  │  │
  │  └─ Método save() genera:
  │     └─ nombre_completo = "Juan García López"
  │
  ├─ Guarda en base de datos
  │  │
  │  └─ INSERT INTO personal_empleados
  │     (usuario, email, apellido_paterno, apellido_materno, nombre, nombre_completo, ...)
  │     VALUES ('jgarcia', 'jgarcia@empresa.com', 'García', 'López', 'Juan', 'Juan García López', ...)
  │
  ├─ Redirige a ver_empleado
  │
  ├─ Usuario ve confirmación con nombre_completo
  │
  └─ END ✅

```

---

## Flujo de Edición de Empleado

```
START
  │
  ├─ Usuario accede a /empleados/editar/1/
  │
  ├─ Servidor carga PersonalEmpleados (id=1) del DB
  │  │
  │  └─ Datos guardados:
  │     ├─ apellido_paterno: "García"
  │     ├─ apellido_materno: "López"
  │     ├─ nombre: "Juan"
  │     └─ nombre_completo: "Juan García López"
  │
  ├─ Renderiza editar_empleado.html
  │  │
  │  └─ Campos pre-cargados:
  │     ├─ Apellido Paterno: [García]
  │     ├─ Apellido Materno: [López]
  │     ├─ Nombre(s): [Juan]
  │     └─ Preview: "Juan García López"
  │
  ├─ Navegador carga nombre-completo.js
  │  │
  │  └─ ejecuta generarNombreCompleto()
  │     └─ Actualiza preview con valores actuales ✅
  │
  ├─ Usuario modifica: Apellido Materno [López] → [Martínez]
  │  │
  │  └─ nombre-completo.js detecta 'keyup'
  │     └─ Preview: "Juan García Martínez" ✅ ACTUALIZADO
  │
  ├─ Usuario hace clic en [GUARDAR]
  │
  ├─ Formulario se envía (POST)
  │
  ├─ Django recibe POST en editar_empleado
  │  │
  │  ├─ PersonalEmpleadosForm valida datos
  │  │  ├─ apellido_paterno: "García" ✅
  │  │  ├─ apellido_materno: "Martínez" ✅ [MODIFICADO]
  │  │  ├─ nombre: "Juan" ✅
  │  │  └─ Otros campos... ✅
  │  │
  │  └─ Form es válido
  │
  ├─ Obtiene instancia PersonalEmpleados (id=1)
  │
  ├─ Actualiza campos desde formulario
  │  │
  │  └─ apellido_materno = "Martínez"
  │
  ├─ Llama a .save()
  │  │
  │  └─ Método save() regenera:
  │     └─ nombre_completo = "Juan García Martínez" [NUEVO]
  │
  ├─ Guarda cambios en base de datos
  │  │
  │  └─ UPDATE personal_empleados
  │     SET apellido_materno = 'Martínez', nombre_completo = 'Juan García Martínez'
  │     WHERE id_empleado = 1
  │
  ├─ Redirige a ver_empleado
  │
  ├─ Usuario ve confirmación con nombre actualizado
  │  │
  │  └─ "Juan García Martínez" ✅
  │
  └─ END ✅

```

---

## Estructura de Base de Datos (Antes vs Después)

### ANTES
```sql
personal_empleados
├─ id_empleado (PK)
├─ usuario (UNIQUE)
├─ email (UNIQUE)
├─ nombre_completo (VARCHAR 200) ← UN SOLO CAMPO
├─ iddepartamento (FK)
├─ idpuesto (FK)
├─ idtipodecontratacion (FK)
└─ ... otros campos ...
```

**Problema**: Nombre es ambiguo, imposible separar componentes

### DESPUÉS
```sql
personal_empleados
├─ id_empleado (PK)
├─ usuario (UNIQUE)
├─ email (UNIQUE)
├─ apellido_paterno (VARCHAR 100) ← NUEVO ✅
├─ apellido_materno (VARCHAR 100, NULL) ← NUEVO ✅
├─ nombre (VARCHAR 100) ← NUEVO ✅
├─ nombre_completo (VARCHAR 200) ← AUTOGENERADO, NO EDITABLE ✅
├─ iddepartamento (FK)
├─ idpuesto (FK)
├─ idtipodecontratacion (FK)
└─ ... otros campos ...
```

**Solución**: 
- Componentes separados y validables
- nombre_completo generado automáticamente
- Datos consistentes garantizados

---

## Interacción entre Componentes

```
┌──────────────────┐
│    Navegador     │
│                  │
│ HTML Formulario  │
│ + Bootstrap CSS  │
│ + JavaScript     │
└────────┬─────────┘
         │ Eventos de usuario
         │ (keyup, change, submit)
         ↓
┌──────────────────────────────────┐
│  nombre-completo.js              │
│  ────────────────────────────── │
│  • Escucha cambios de campos    │
│  • Genera nombre_completo       │
│  • Actualiza preview            │
│  • Valida antes de enviar       │
└────────┬────────────────────────┘
         │ Form submit (POST)
         ↓
┌──────────────────────────────────┐
│  Django View                     │
│  (crear_empleado / editar_empleado)
│  ────────────────────────────── │
│  • Recibe POST                  │
│  • Instancia formulario         │
│  • Valida datos                 │
└────────┬────────────────────────┘
         │ Valida
         ↓
┌──────────────────────────────────┐
│  PersonalEmpleadosForm           │
│  ────────────────────────────── │
│  • Valida cada campo            │
│  • Limpia datos                 │
│  • Retorna instancia            │
└────────┬────────────────────────┘
         │ Si válido
         ↓
┌──────────────────────────────────┐
│  PersonalEmpleados.save()        │
│  ────────────────────────────── │
│  • Genera nombre_completo       │
│  • Ejecuta pre-save             │
│  • Guarda en DB                 │
└────────┬────────────────────────┘
         │ INSERT/UPDATE
         ↓
┌──────────────────────────────────┐
│  MySQL/MariaDB                   │
│  personal_empleados table        │
│  ────────────────────────────── │
│  • Almacena 7 campos de nombre  │
│  • Indexado por nombre_completo │
│  • Integridad referencial       │
└────────┬────────────────────────┘
         │ Query result
         ↓
┌──────────────────────────────────┐
│  Respuesta Django                │
│  ────────────────────────────── │
│  • Redirect a ver_empleado      │
│  • O retorna JSON (AJAX)        │
└────────┬────────────────────────┘
         │ HTTP Response
         ↓
┌──────────────────┐
│  Navegador       │
│  ────────────── │
│  • Muestra      │
│    confirmación │
│  • Renderiza    │
│    vista        │
└──────────────────┘
```

---

## Tecnologías Utilizadas

```
┌─────────────────────────────────────────────────────┐
│              STACK TECNOLÓGICO                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Backend:                                          │
│  ├─ Django 6.0.2                                   │
│  ├─ Python 3.x                                     │
│  ├─ Django ORM                                     │
│  └─ Django Forms                                   │
│                                                     │
│  Base de Datos:                                    │
│  ├─ MySQL/MariaDB (vía XAMPP)                      │
│  ├─ 1 tabla modificada (personal_empleados)        │
│  └─ Índices automáticos en PK/FK                   │
│                                                     │
│  Frontend:                                         │
│  ├─ HTML5                                          │
│  ├─ Bootstrap 5                                    │
│  ├─ JavaScript (vanilla, sin librerías)            │
│  └─ CSS3                                           │
│                                                     │
│  Herramientas de Desarrollo:                       │
│  ├─ manage.py (Django management)                  │
│  ├─ Migraciones (Django)                           │
│  ├─ Admin interface (Django)                       │
│  └─ Django Debug Toolbar                           │
│                                                     │
│  Infraestructura:                                  │
│  ├─ XAMPP (Apache + MySQL + PHP)                   │
│  ├─ Windows (SO anfitrión)                         │
│  └─ VS Code (Editor)                               │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## Ejemplo de Datos Guardados

```json
{
  "id_empleado": 42,
  "usuario": "jgarcia",
  "email": "jgarcia@empresa.com",
  "apellido_paterno": "García",
  "apellido_materno": "López",
  "nombre": "Juan",
  "nombre_completo": "Juan García López",
  "curp": "GAGL800315HDFRR04",
  "rfc": "GAGL8003154K2",
  "fecha_nacimiento": "1980-03-15",
  "sexo": "M",
  "telefono": "5551234567",
  "domicilio": "Calle Principal 123, Apt. 4, Mexico City",
  "fotografia": "empleados/fotos/jgarcia.jpg",
  "iddepartamento": 3,
  "departamento": "Dirección Comercial",
  "idpuesto": 5,
  "puesto": "Gerente de Ventas",
  "numero_empleado": "EMP-2024-042",
  "fecha_ingreso": "2024-01-15",
  "idtipodecontratacion": 1,
  "tipo_contratacion": "Sindical",
  "salario": 50000.00,
  "activo": true,
  "fecha_creacion": "2024-03-03T15:30:00Z",
  "fecha_modificacion": "2024-03-03T15:30:00Z"
}
```

---

## Conclusión Visual

```
                    ✅ IMPLEMENTACIÓN COMPLETADA
                    
    Antes              →              Después
    
┌─────────────────┐             ┌──────────────────┐
│ nombre_completo │             │ apellido_paterno │
│ [Una caja]      │    ====>    │ apellido_materno │
│ Ambiguo         │             │ nombre           │
│ No validable    │             │ nombre_completo  │
└─────────────────┘             │ (autogenerado)   │
                                └──────────────────┘
                                Claro, validable,
                                automatizado

Estado: ✅ LISTO PARA PRODUCCIÓN
```

