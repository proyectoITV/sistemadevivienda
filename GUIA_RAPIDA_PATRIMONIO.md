# Guía de Inicio Rápido - Módulo de Patrimonio

## 🚀 Para Comenzar

### 1. Iniciar el Servidor Django
```bash
python manage.py runserver
```

### 2. Acceder a la Aplicación
Abre tu navegador en:
```
http://127.0.0.1:8000/
```

### 3. Iniciar Sesión
- Usuario: (tu usuario del sistema)
- Contraseña: (tu contraseña)

### 4. Acceder al Módulo de Patrimonio

#### Opción A: Usando el Menú
1. En el dashboard, busca **"Dirección de Administración"**
2. Expande el menú si está contraído
3. Selecciona **"Recursos Humanos"**
4. Expande **"Patrimonio"**
5. Haz clic en **"Bienes del Instituto"**

#### Opción B: URL Directa
```
http://127.0.0.1:8000/patrimonio/bienes/
```

---

## 📋 Operaciones Básicas

### Crear un Nuevo Bien

1. Haz clic en el botón **"+ Nuevo Bien"** en la esquina superior derecha
2. Completa el formulario:
   - **Número Inventario ITAVU** (requerido) - Ej: ITAVU-2024-001
   - **Número Inventario Gobierno** (opcional)
   - **Descripción** (requerido) - Ej: "Laptop Dell Latitude"
   - **Marca** - Selecciona de la lista
   - **Modelo** - Ej: "Latitude 7550"
   - **Número de Serie** - El número del fabricante
   - **Fotografía** - Sube una foto si lo deseas
   - **Fecha de Factura**
   - **Número de Factura**
   - **Costo del Artículo** (requerido) - Ej: 15000.00
   - **Proveedor** - Selecciona de la lista
   - **Clasificación SERAP** - Ej: "Equipo de computo"
   - **Clasificación Contraloría** - Ej: "Bien inventariable"
   - **Observaciones** - Notas adicionales
   - **Activo** - Marca si está en uso

3. Haz clic en **"Guardar"**

### Buscar un Bien

1. En la lista de bienes, usa la barra de búsqueda superior
2. Escribe parte de:
   - Número inventario ITAVU
   - Número inventario gobierno
   - Descripción
   - Número de serie
   - Número de factura
3. Haz clic en **"Buscar"** o presiona Enter

### Filtrar por Estado

1. En la lista, selecciona el estado:
   - "Todos los estados"
   - "Activos"
   - "Inactivos"
2. Haz clic en **"Buscar"**

### Editar un Bien

1. Encuentra el bien en la lista
2. Haz clic en el botón **"Editar"** (icono de lápiz)
3. Modifica los campos que desees
4. Haz clic en **"Guardar"**

### Cambiar Estado de un Bien

1. Encuentra el bien en la lista
2. Haz clic en el botón **"Cambiar Estado"** (icono de toggle)
3. El estado se invierte automáticamente (Activo → Inactivo o vice versa)

---

## 📊 Datos Precargados

El sistema viene con datos iniciales:

### Marcas Disponibles
- HP
- Dell
- Lenovo
- Asus
- Apple
- Canon
- Epson
- Samsung
- LG
- Xerox
- Office Depot
- Steelcase

### Clasificaciones SERAP
- Equipo de comunicación
- Equipo de computo
- Herramienta
- Mobiliario y equipo de oficina

### Clasificaciones de Contraloría
- Bien controlable
- Bien controlable - gasto
- Bien inventariable
- Bienes baja definitiva

### Proveedores
- Ingram Micro
- Softland
- Grupo Econom
- Muebles Corporativos

---

## 💡 Consejos y Mejores Prácticas

1. **Número de Inventario ITAVU**: Use un formato consistente
   - Ej: ITAVU-2024-001, ITAVU-2024-002, etc.

2. **Fotografías**: Use fotos claras de la etiqueta o del artículo

3. **Serie**: Si el bien no tiene número de serie, déjelo vacío

4. **Datos de Factura**: Importante para auditoría y depreciación

5. **Clasificaciones**: Seleccione ambas (SERAP y Contraloría) cuando sea posible

6. **Observaciones**: Use este campo para notas sobre:
   - Ubicación física
   - Asignación a empleado
   - Estado de conservación
   - Próximo mantenimiento

---

## ⚠️ Validaciones

El sistema verifica automáticamente:

- ✅ Número de Inventario ITAVU: Debe ser único
- ✅ Descripción: Debe estar completa
- ✅ Costo: Debe ser un número positivo
- ✅ Número de Serie: Debe ser único si se proporciona
- ✅ Número de Factura: Debe ser único si se proporciona
- ✅ Fotografía: Solo acepta archivos de imagen

---

## 🔄 Flujo de Trabajo Típico

```
1. Ingresa nueva compra → 2. Carga foto → 3. Ingresa datos técnicos
                              ↓
                     4. Asigna clasificaciones
                              ↓
                     5. Marca como Activo
                              ↓
                     6. El bien ya está en inventario
```

---

## 📞 ¿Problemas?

### El menú no muestra Patrimonio
- Asegúrate de estar autenticado
- Recarga la página (F5)
- Limpia caché del navegador

### No puedo crear un bien
- Verifica que completaste todos los campos requeridos (marcados con *)
- Asegúrate que el Número Inventario ITAVU sea único
- Comprueba la conexión a la base de datos

### Los datos no se guardaron
- Verifica que no haya mensajes de error en rojo
- Intenta de nuevo
- Si persiste, contacta al soporte

### ¿Necesitas ayuda adicional?
Revisa el archivo `DOCUMENTACION_PATRIMONIO.md` para más detalles técnicos.

---

## 📄 Archivos Importantes

- `DOCUMENTACION_PATRIMONIO.md` - Documentación técnica completa
- `RESUMEN_PATRIMONIO.md` - Resumen de implementación
- `cargar_patrimonio.py` - Script para cargar datos iniciales
- `verificar_patrimonio.py` - Script para verificar configuración

---

**¡Listo para usar! Accede a tu módulo de Patrimonio ahora mismo.**
