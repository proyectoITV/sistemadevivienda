# Implementación de Campos de Oficio en Resguardos Internos

## 🎯 Objetivo
Agregar campos para gestionar información de oficios (documentos gubernamentales) en el sistema de resguardos internos, permitiendo registrar y descargar PDFs de oficios asociados a la asignación de bienes.

## 📋 Cambios Realizados

### 1. **Modelo - `PatrimonioResguardo`** 
**Archivo:** `anuncios/models.py`

Tres nuevos campos agregados:
```python
numero_oficio = models.CharField(max_length=100, blank=True)
fecha_oficio = models.DateField(null=True, blank=True)
archivo_oficio = models.FileField(upload_to='patrimonio/oficios/', null=True, blank=True)
```

**Validaciones:**
- `numero_oficio`: Hasta 100 caracteres, opcional
- `fecha_oficio`: Campo de fecha, opcional
- `archivo_oficio`: Almacenado en `media/patrimonio/oficios/`, solo PDFs

---

### 2. **Formulario - `PatrimonioResguardoAsignacionForm`**
**Archivo:** `anuncios/forms.py`

**Campos agregados:**
- `numero_oficio`: TextInput con placeholder "Ej: OF-2026-001"
- `fecha_oficio`: DateInput
- `archivo_oficio`: FileInput con validación personalizada

**Método de Validación - `clean_archivo_oficio()`:**
```python
def clean_archivo_oficio(self):
    archivo = self.cleaned_data.get('archivo_oficio')
    if archivo:
        # Validar extensión: solo .pdf
        if not archivo.name.lower().endswith('.pdf'):
            raise ValidationError('El archivo debe ser un PDF.')
        
        # Validar tamaño: máximo 10 MB
        if archivo.size > 10485760:  # 10 MB en bytes
            raise ValidationError('El archivo no debe exceder 10 MB.')
    
    return archivo
```

---

### 3. **Vistas - Nueva Vista para Descargar Oficio**
**Archivo:** `anuncios/views.py`

**Nueva Vista:** `descargar_oficio_resguardo()`
- **URL:** `/patrimonio/resguardos/<idresguardo>/descargar-oficio/`
- **Decorador:** `@login_required`
- **Funcionalidad:**
  - Valida que el resguardo existe
  - Valida que el usuario está autenticado
  - Verifica que el archivo existe en el servidor
  - Descarga el PDF con nombre: `OF_[numero_oficio].pdf`

**Ejemplo de flujo:**
```
1. Usuario hace clic en "Descargar PDF"
2. Vista valida permisos y existencia del archivo
3. Descarga el PDF con nombre legible
```

---

### 4. **URLs - Ruta de Descarga**
**Archivo:** `anuncios/urls.py`

Ruta agregada:
```python
path('patrimonio/resguardos/<int:idresguardo>/descargar-oficio/', 
     views.descargar_oficio_resguardo, 
     name='descargar_oficio_resguardo'),
```

---

### 5. **Plantillas - Interfaz de Usuario**

#### a) **Lista de Resguardos**
**Archivo:** `anuncios/templates/anuncios/patrimonio/listar_resguardos.html`

**Cambios:**
- Nueva columna "Oficio" en la tabla
- Muestra número de oficio si existe
- Botón "PDF" para descargar (si el archivo existe)
- Ejemplo:
  ```html
  <td>
      {% if resguardo.numero_oficio %}
          <div>{{ resguardo.numero_oficio }}</div>
          {% if resguardo.archivo_oficio %}
              <a href="{% url 'descargar_oficio_resguardo' resguardo.idresguardo %}" 
                 class="btn btn-sm btn-outline-danger">
                  <i class="fas fa-download"></i> PDF
              </a>
          {% endif %}
      {% else %}
          <span class="text-muted">-</span>
      {% endif %}
  </td>
  ```

#### b) **Historial de Resguardos (Por Bien)**
**Archivo:** `anuncios/templates/anuncios/patrimonio/historial_resguardo_bien.html`

**Cambios:**
- Nueva columna "Oficio" entre "Fecha Asignación" y "Fecha Devolución"
- Misma funcionalidad de visualización y descarga

#### c) **Historial de Resguardos (Por Empleado)**
**Archivo:** `anuncios/templates/anuncios/patrimonio/historial_resguardo_empleado.html`

**Cambios:**
- Nueva columna "Oficio" en la tabla
- Descarga de PDF directa

#### d) **Formulario de Asignación**
**Archivo:** `anuncios/templates/anuncios/patrimonio/form_resguardo_asignacion.html`

**Cambios:**
- Enctype cambiado a `multipart/form-data`
- Nueva sección "Información del Oficio (Opcional)"
- Campos:
  - Número de Oficio (texto)
  - Fecha del Oficio (fecha)
  - Archivo del Oficio (archivo PDF)
- Validaciones en JavaScript (opcional, carga máxima mostrada)

---

### 6. **Migración**
**Archivo:** `anuncios/migrations/0024_agregar_campos_oficio_resguardo.py`

Migración automática que:
- Agrega campo `numero_oficio` (CharField, max_length=100)
- Agrega campo `fecha_oficio` (DateField)
- Agrega campo `archivo_oficio` (FileField)

**Ejecución:**
```bash
python manage.py migrate anuncios
```

---

## 🔐 Seguridad y Validaciones

### 1. **Validación de Archivo**
- Solo se aceptan archivos `.pdf`
- Tamaño máximo: 10 MB
- Error si incumple: Mensaje de validación en el formulario

### 2. **Acceso a Descargas**
- Requiere `@login_required`
- Valida que el usuario esté autenticado
- Verifica que el archivo existe antes de descargar

### 3. **Almacenamiento**
- Carpeta dedicada: `media/patrimonio/oficios/`
- Nombres de archivo: Generados automáticamente por Django
- Descargas: Con nombre legible `OF_[numero].pdf`

---

## 📁 Estructura de Carpetas

```
media/
└── patrimonio/
    └── oficios/
        ├── [archivo_uuid_1].pdf
        ├── [archivo_uuid_2].pdf
        └── ...
```

---

## 🧪 Pruebas Recomendadas

### Test 1: Asignación de Resguardo con Oficio
1. Ir a "Asignar Resguardo"
2. Completar formulario
3. Agregar:
   - Número de Oficio: "OF-2026-001"
   - Fecha de Oficio: 06/03/2026
   - Archivo: Seleccionar PDF válido
4. Guardar y verificar que aparece en lista

### Test 2: Descarga de PDF
1. Ir a "Resguardos Internos"
2. Buscar resguardo con oficio
3. Hacer clic en botón "PDF"
4. Verificar que se descarga con nombre correcto

### Test 3: Validación de Archivo
1. Intentar subir archivo que no es PDF (ej: .txt)
2. Verificar que muestra error: "El archivo debe ser un PDF"
3. Intentar subir PDF > 10 MB
4. Verificar que muestra error: "El archivo no debe exceder 10 MB"

### Test 4: Historial
1. Ir a "Ver Historial del Bien"
2. Verificar que columna "Oficio" aparece
3. Descargar PDF desde historial
4. Repetir con historial del empleado

---

## 🔧 Configuración de Servidor

**Asegúrese que en `core/settings.py`:**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

**En `core/urls.py` para desarrollo:**
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                         document_root=settings.MEDIA_ROOT)
```

---

## 📊 Resumen Técnico

| Aspecto | Detalle |
|---------|---------|
| **Campos agregados** | 3 (numero_oficio, fecha_oficio, archivo_oficio) |
| **Validaciones** | Extensión PDF, tamaño máximo 10 MB |
| **Rutas nuevas** | 1 (`descargar_oficio_resguardo`) |
| **Vistas nuevas** | 1 (`descargar_oficio_resguardo()`) |
| **Plantillas actualizadas** | 4 (listar, historial bien, historial empleado, formulario) |
| **Migración | 0024_agregar_campos_oficio_resguardo |
| **Seguridad** | @login_required, validaciones en cliente y servidor |

---

## ✅ Estado de Implementación

- ✅ Modelo actualizado con 3 campos
- ✅ Formulario con validación de PDF
- ✅ Vista de descarga implementada
- ✅ URLs configuradas
- ✅ 4 plantillas actualizadas
- ✅ Migración creada y aplicada
- ✅ Servidor corriendo sin errores
- ✅ Sistema listo para pruebas

---

## 🚀 Próximos Pasos Opcionales

1. **Reportes**: Agregar opción para generar reportes de oficios por período
2. **Auditoría**: Registrar descargas de oficios para auditoría
3. **Validación adicional**: Validar número de oficio con formato específico
4. **Plantilla PDF**: Generar certificados de resguardo con información del oficio

---

**Fecha de Implementación:** 06 de Marzo de 2026
**Desarrollador:** Sistema de Vivienda ITAVU
**Estado:** ✅ Operacional
