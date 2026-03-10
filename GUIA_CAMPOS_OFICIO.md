# 📖 GUÍA DE USO - CAMPOS DE OFICIO EN RESGUARDOS

## 🎯 Objetivo
Esta guía explica cómo usar los nuevos campos de oficio en el sistema de resguardos internos.

---

## 📚 Tabla de Contenidos
1. [Conceptos Básicos](#conceptos-básicos)
2. [Asignar Resguardo con Oficio](#asignar-resguardo-con-oficio)
3. [Descargar Oficios](#descargar-oficios)
4. [Ver Historial](#ver-historial)
5. [Preguntas Frecuentes](#preguntas-frecuentes)

---

## Conceptos Básicos

### ¿Qué es un Oficio?
Un **oficio** es un documento oficial del gobierno que autoriza la asignación de un bien a un empleado. El sistema permite:
- Registrar el número del oficio
- Guardar la fecha del oficio
- Almacenar el PDF del oficio
- Descargar el PDF cuando sea necesario

### ¿Dónde se almacenan los archivos?
Los archivos PDF se guardan en: `media/patrimonio/oficios/`

### ¿Son obligatorios los campos de oficio?
**No.** Los campos son **opcionales**. Puede asignar bienes sin oficio si es necesario.

---

## Asignar Resguardo con Oficio

### Opción 1: Con Interfaz Web (Recomendado)

#### Paso 1: Acceder a Resguardos Internos
```
Dashboard
  ↓
Administración
  ↓
Patrimonio
  ↓
Resguardos Internos
```

#### Paso 2: Hacer Clic en "Asignar Resguardo"
- Botón verde con icono de "+"
- Se abre formulario de asignación

#### Paso 3: Completar Datos del Bien y Empleado
```
┌─────────────────────────────────────┐
│ FORMULARIO DE ASIGNACIÓN            │
├─────────────────────────────────────┤
│                                     │
│ Bien: [________________________]    │  ← Usar Select2
│       (Buscar por No. Inventario)   │
│                                     │
│ Empleado: [____________________]    │  ← Usar Select2
│          (Buscar por número/nombre) │
│                                     │
│ Fecha Asignación: [________________]│  ← Selector de fecha
│                                     │
└─────────────────────────────────────┘
```

**Ejemplo:**
- **Bien:** `INV-2026-001` - Computadora Dell
- **Empleado:** `EMP-002` - Juan Pérez García
- **Fecha:** 06/03/2026

#### Paso 4: Llenar Información del Oficio
```
┌─────────────────────────────────────┐
│ INFORMACIÓN DEL OFICIO (Opcional)   │
├─────────────────────────────────────┤
│                                     │
│ Número Oficio: [_________________]  │
│ Ej: OF-2026-001                     │
│                                     │
│ Fecha Oficio: [__________________]  │
│ (Selector de fecha)                 │
│                                     │
│ Archivo Oficio: [_________________] │
│ (Solo PDF, máx 10 MB)               │
│ [   Seleccionar Archivo   ]          │
│                                     │
└─────────────────────────────────────┘
```

**Ejemplo:**
```
Número Oficio: OF-ADM-2026-001
Fecha Oficio:  06/03/2026
Archivo:       OFICIO_ASIGNACION_BIEN_001.pdf
```

#### Paso 5: Observaciones (Opcional)
```
┌─────────────────────────────────────┐
│ Observaciones Asignación:           │
│                                     │
│ [_______________________________]    │
│ [_______________________________]    │
│                                     │
│ "Bien asignado por la Dirección..."│
│                                     │
└─────────────────────────────────────┘
```

#### Paso 6: Guardar
- Botón azul: "Guardar Resguardo"
- Sistema validará:
  - ✓ Que el bien existe
  - ✓ Que el empleado existe
  - ✓ Que el archivo es PDF (si se subió)
  - ✓ Que el archivo no excede 10 MB

---

### Opción 2: Sin Oficio
Si no tiene oficio aún, puede dejar los campos en blanco y agregar después.

```
Número Oficio: [VACÍO]
Fecha Oficio:  [VACÍO]
Archivo:       [VACÍO]
```

El sistema mostrará "-" en esos campos.

---

## Descargar Oficios

### Desde Lista de Resguardos

#### Paso 1: Ir a Resguardos Internos
```
Dashboard → Administración → Patrimonio → Resguardos Internos
```

#### Paso 2: Buscar el Resguardo
```
┌─────────────────────────────────────────────────┐
│ Buscar por bien, inventario o empleado...       │
│ [___________________________]  [Buscar]         │
│                                                 │
│ Estado: [Activos ▼]                             │
└─────────────────────────────────────────────────┘
```

#### Paso 3: Encontrar Oficio en Tabla
```
┌─────────────────────────────────────────────────────────┐
│ No. Inv │ Bien │ Empleado │ Fecha │ OFICIO │ Acciones │
├─────────────────────────────────────────────────────────┤
│ INV-001 │ ... │   ...    │ ...   │ OF-... │ PDF ⬇️  │
│ INV-002 │ ... │   ...    │ ...   │   -    │  -      │
│ INV-003 │ ... │   ...    │ ...   │ OF-... │ PDF ⬇️  │
└─────────────────────────────────────────────────────────┘
```

#### Paso 4: Hacer Clic en "PDF"
- Se descarga el archivo
- Nombre: `OF_[numero_oficio].pdf`

**Ejemplo:**
```
Descarga: OF_OF-2026-001.pdf
Ubicación: Descargas (según navegador)
```

---

### Desde Historial del Bien

#### Acceso:
```
1. En lista de resguardos
2. Hacer clic en icono 📜 (historial del bien)
3. Se abre ventana con historial
```

#### Descargar:
```
┌────────────────────────────────────┐
│ HISTORIAL DEL BIEN                 │
├────────────────────────────────────┤
│ Empleado │ Asignación │ OFICIO     │
├────────────────────────────────────┤
│ Juan P.  │ 06/03/2026 │ OF-...     │
│          │            │ [PDF ⬇️]   │ ← Clic aquí
│          │            │            │
│ María L. │ 15/01/2026 │ -          │
│          │            │ (sin oficio)│
└────────────────────────────────────┘
```

---

### Desde Historial del Empleado

#### Acceso:
```
1. En lista de resguardos
2. Hacer clic en icono 📜 (historial del empleado)
3. Se abre ventana con historial
```

#### Descargar:
```
┌────────────────────────────────────┐
│ HISTORIAL DEL EMPLEADO             │
├────────────────────────────────────┤
│ Bien │ Asignación │ OFICIO         │
├────────────────────────────────────┤
│ Compu│ 06/03/2026 │ OF-ADM-001     │
│      │            │ [PDF ⬇️]       │ ← Clic aquí
│      │            │                │
│ Mouse│ 15/01/2026 │ -              │
│      │            │ (sin oficio)    │
└────────────────────────────────────┘
```

---

## Ver Historial

### Historial Completo del Bien

**Acceso:**
```
Dashboard → Patrimonio → Resguardos → [clic en icono] → Historial
```

**Información Mostrada:**
```
┌─────────────────────────────────────────────────────────┐
│ HISTORIAL DEL BIEN: INV-2026-001                        │
│ Computadora Dell XPS 13                                 │
├─────────────────────────────────────────────────────────┤
│ Empleado │ Asignación │ Oficio  │ Devolución │ Días    │
├─────────────────────────────────────────────────────────┤
│ Juan P.  │ 06/03/2026 │OF-001   │ -          │ 30 días │
│          │            │PDF ⬇️   │ en uso     │ aprox   │
│          │            │         │            │         │
│ María L. │ 15/01/2026 │OF-002   │ 05/02/2026 │ 21 días │
│          │            │PDF ⬇️   │            │         │
│          │            │         │            │         │
│ Carlos R.│ 01/12/2025 │ -       │ 14/12/2025 │ 13 días │
│          │            │         │            │         │
└─────────────────────────────────────────────────────────┘
```

**Análisis del Historial:**
- **Juan P. (Activo):** Tiene el bien desde 06/03/2026 con Oficio OF-001
- **María L.:** Tuvo el bien 21 días con Oficio OF-002
- **Carlos R.:** Tuvo el bien 13 días sin oficio

---

### Historial Completo del Empleado

**Acceso:**
```
Dashboard → Patrimonio → Resguardos → [clic en icono empleado] → Historial
```

**Información Mostrada:**
```
┌────────────────────────────────────────────────────────┐
│ HISTORIAL DEL EMPLEADO: Juan Pérez García              │
├────────────────────────────────────────────────────────┤
│ Bien      │ Asignación │ Oficio   │ Devolución │ Estado│
├────────────────────────────────────────────────────────┤
│ Compu     │ 06/03/2026 │OF-001    │ -          │Activo │
│ Dell XPS  │            │PDF ⬇️    │ en uso     │       │
│           │            │          │            │       │
│ Mouse     │ 15/01/2026 │OF-002    │ 05/02/2026 │Devuelto│
│ Logitech  │            │PDF ⬇️    │            │       │
│           │            │          │            │       │
│ Monitor   │ 01/12/2025 │-         │ 14/12/2025 │Devuelto│
│ Samsung   │            │          │            │       │
└────────────────────────────────────────────────────────┘
```

**Análisis:**
- **Computadora Dell:** Activa desde 06/03/2026 con Oficio
- **Mouse Logitech:** Devuelta con Oficio (21 días)
- **Monitor Samsung:** Devuelta sin Oficio (13 días)

---

## Preguntas Frecuentes

### P1: ¿Puedo cambiar el oficio después de asignar?
**R:** No directamente. El sistema es de auditoría. Si necesita cambiar:
1. Devolver el bien
2. Asignar de nuevo con nuevo oficio

### P2: ¿Qué pasa si subo un archivo que no es PDF?
**R:** El sistema muestra error:
```
"El archivo debe ser un PDF."
```
Convierta el archivo a PDF e intente de nuevo.

### P3: ¿Cuál es el tamaño máximo del PDF?
**R:** 10 MB (10,485,760 bytes)

Si el archivo es mayor, el sistema muestra:
```
"El archivo no debe exceder 10 MB."
```

### P4: ¿Qué formato debe tener el número de oficio?
**R:** Cualquier formato. Ejemplos válidos:
- `OF-2026-001`
- `ADM-100-2026`
- `20260306-001`
- `OFICIO-123`

### P5: ¿Puedo descargar un oficio múltiples veces?
**R:** Sí. No hay límite de descargas.

### P6: ¿Qué usuarios pueden descargar oficios?
**R:** Solo usuarios autenticados (con login).

### P7: ¿Dónde se guardan los archivos?
**R:** En: `media/patrimonio/oficios/`

Los archivos se renombran automáticamente para seguridad.

### P8: ¿Puedo eliminar un oficio?
**R:** No. El sistema no permite eliminar oficios (auditoría).

Si necesita, devuelva el bien y asigne de nuevo.

### P9: ¿Qué pasa si borro el archivo accidentalmente?
**R:** El sistema mostrará:
```
"El archivo del oficio no se encuentra en el servidor."
```

Contacte al administrador para recuperación.

### P10: ¿Se puede exportar el historial con oficios?
**R:** Actualmente no. Puede:
1. Captura de pantalla (Print Screen)
2. Imprimir desde navegador (Ctrl+P)
3. Copiar datos manualmente

---

## 🔒 Seguridad y Privacidad

### Acceso Controlado
- ✅ Solo usuarios autenticados
- ✅ Requiere credenciales válidas
- ✅ Se registra en auditoría

### Almacenamiento Seguro
- ✅ Carpeta dedicada: `patrimonio/oficios/`
- ✅ Nombres de archivo generados aleatoriamente
- ✅ Protegido de acceso directo desde web

### Integridad de Datos
- ✅ No se permite eliminar oficios
- ✅ Se mantiene histórico completo
- ✅ Auditoría de cambios

---

## ⚡ Tips y Trucos

### Tip 1: Usar Select2 Efectivamente
```
Cuando ingrese bien o empleado:
- Escriba número (ej: INV-2026)
- O nombre (ej: Computadora)
- Sistema filtra automáticamente
- Seleccione de la lista
```

### Tip 2: Buscar en Historial
```
Si tiene muchos resguardos:
1. Use filtros (Activos/Devueltos/Todos)
2. Use búsqueda por bien o empleado
3. Haga clic en historial para detalles
```

### Tip 3: Preparar PDFs
```
Antes de subir:
1. Asegurar que es PDF válido
2. Verificar tamaño < 10 MB
3. Usar nombre descriptivo
4. Guardar en carpeta de descarga
```

### Tip 4: Generar Número de Oficio
```
Formato sugerido:
OF-[AÑO]-[NÚMERO SECUENCIAL]

Ejemplos:
- OF-2026-001 (primer oficio 2026)
- OF-2026-002 (segundo oficio 2026)
- OF-2026-100 (centésimo oficio 2026)
```

### Tip 5: Documentación
```
Guarde en observaciones:
- Motivo de la asignación
- Nombre de quien autoriza
- Departamento origen
- Observaciones especiales
```

---

## 📞 Soporte y Ayuda

### Si experimenta problemas:

**Problema:** No puedo subir el PDF
```
Solución:
1. Verificar que sea PDF (.pdf)
2. Verificar tamaño < 10 MB
3. Intentar con otro navegador
```

**Problema:** No puedo descargar
```
Solución:
1. Verificar que está autenticado
2. Verificar que el resguardo tiene oficio
3. Revisar la columna "Oficio"
4. Contactar administrador
```

**Problema:** El archivo no aparece
```
Solución:
1. Guardar el formulario nuevamente
2. Refrescar la página (F5)
3. Limpiar caché (Ctrl+Shift+Delete)
4. Contactar administrador
```

---

## 📋 Checklist para Asignar Resguardo

```
☐ Identificar el bien a asignar
☐ Identificar el empleado destinatario
☐ Obtener el número del oficio
☐ Obtener la fecha del oficio
☐ Tener el PDF del oficio listo
☐ Verificar que PDF < 10 MB
☐ Acceder al formulario de asignación
☐ Completar datos del bien
☐ Completar datos del empleado
☐ Ingresar número del oficio
☐ Ingresar fecha del oficio
☐ Seleccionar archivo PDF
☐ Completar observaciones (opcional)
☐ Hacer clic en "Guardar"
☐ Verificar confirmación de éxito
☐ Ir a historial para confirmar
```

---

## 🎓 Capacitación Básica

**Duración:** 15 minutos
**Requisitos:** Acceso al sistema

### Sesión 1 (5 min): Conceptos
- ¿Qué es un oficio?
- ¿Dónde se guardan?
- Validaciones

### Sesión 2 (5 min): Asignación
- Navegar a formulario
- Completar campos
- Subir archivo

### Sesión 3 (5 min): Descarga
- Encontrar en lista
- Descargar desde historial
- Resolver problemas

---

**Última actualización:** 06/03/2026
**Versión:** 1.0
**Estado:** ✅ Vigente
