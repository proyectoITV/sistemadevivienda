# 🚀 PRÓXIMOS PASOS - Sistema de Cola de Correos

## ⚠️ ACCIÓN INMEDIATA REQUERIDA

### PASO 1: Aplicar Migración a Base de Datos (CRÍTICO)

```bash
cd c:\xampp\htdocs\Desarrollos\ web\sistemadevivienda

# Ejecutar migración
python manage.py migrate anuncios 0018
```

**Salida esperada:**
```
Operations to perform:
  Apply 1 migration: anuncios.0018_colacorreos
Running migrations:
  Applying anuncios.0018_colacorreos... OK
```

**Verificar que funcionó:**
```bash
python manage.py dbshell
> SELECT COUNT(*) FROM cola_correos;
```

Si ves `0`, ¡la tabla se creó exitosamente!

---

### PASO 2: Ejecutar Script de Verificación

```bash
python verificar_cola_correos.py
```

**Esto validará que todo esté funcionando:**
```
✓ Modelo ColaCorreos encontrado
✓ Correo guardado exitosamente
✓ Correos enviados hoy: 0/2000
✓ Total de correos en cola: 1
✓ Procesamiento completado
✓ Verificación de reintentos OK
✓ Comando 'procesar_cola_correos' existe

Total: 7/7 pruebas exitosas (100%)
✓ ¡TODAS LAS PRUEBAS PASARON!
```

**Si alguna falla:**
1. Revisar el error mostrado
2. Revisar TROUBLESHOOTING en DOCUMENTACION_COLA_CORREOS.md
3. Ejecutar nuevamente

---

### PASO 3: Acceder al Monitor Web

**URL:** http://localhost:8000/seguridad/cola-correos/

**Deberías ver:**
- Tarjetas de estadísticas
- Tabla vacía de correos (aún no hay)
- Botón "Procesar Cola Ahora"

**Si no ves nada:**
- Asegúrate de estar logueado como admin
- Verifica que usuario sea miembro de `UsuariosDelSistema` con rol 'admin'

---

### PASO 4: Probar Funcionalidad

**Test 1: Crear un empleado con credenciales**
```
1. Ir a /empleados/crear/
2. Rellenar formulario:
   - Nombre: "Test Usuario"
   - Usuario: "testuser"
   - Contraseña: "Test123456"
   - Email: "testuser@example.com"
3. Click: [Guardar Empleado]
```

**Verificar en monitor:**
```
1. Ir a /seguridad/cola-correos/
2. Deberías ver 1 correo en tabla
3. Estado: Pendiente (porque SMTP podría no estar configurado)
```

**Test 2: Procesar la cola**
```
1. En monitor, click: [Procesar Cola Ahora]
2. Se abrirá modal "Procesando Cola de Correos..."
3. Verás resultado:
   - Enviados: 1 (si SMTP está configurado)
   - O Pendientes: 1 (si SMTP no está disponible)
```

---

### PASO 5: Configurar Procesamiento Automático

Elegir UNA opción:

#### Opción A: Cron Job (RECOMENDADO)

**Linux/Mac:**
```bash
# Abrir crontab
crontab -e

# Agregar esta línea al final:
*/5 * * * * cd /ruta/al/proyecto && python manage.py procesar_cola_correos --limite 2000 >> /tmp/cola_correos.log 2>&1
```

**Windows - Task Scheduler GUI:**
1. Abrir "Programador de tareas"
2. "Crear tarea básica"
3. Nombre: "ITAVU_Procesar_Cola_Correos"
4. Trigger: "Cada 5 minutos"
5. Acción: Iniciar programa
   - Programa: `C:\xampp\python\python.exe`
   - Argumentos: `C:\ruta\manage.py procesar_cola_correos --limite 2000`
6. Guardar

**Windows - PowerShell Script (procesar_cola.ps1):**
```powershell
$interval = 300  # 5 minutos en segundos
$projectPath = "C:\xampp\htdocs\Desarrollos web\sistemadevivienda"

while($true) {
    Set-Location $projectPath
    python manage.py procesar_cola_correos --limite 2000
    Start-Sleep -Seconds $interval
}
```

Ejecutar con:
```bash
powershell -ExecutionPolicy Bypass -File procesar_cola.ps1
```

#### Opción B: Celery (Para proyectos grandes)

```bash
# Instalar
pip install celery redis

# Crear portal/tasks.py:
from celery import shared_task
from .email_utils import procesar_cola_correos

@shared_task
def procesar_cola_correos_task():
    return procesar_cola_correos(limite_diario=2000)
```

Configurar beat schedule en core/settings.py

#### Opción C: APScheduler (Sin dependencias externas)

```bash
pip install apscheduler
```

Crear en core/apps.py e integrar con Django startup

---

### PASO 6: Configurar Alertas (Opcional)

Si quieres ser notificado cuando la cola crece:

**En /admin/anuncios/colacorreos/, crear vista personalizada**

O ejecutar este comando periódicamente:
```bash
python manage.py shell << EOF
from portal.models import ColaCorreos
pendientes = ColaCorreos.objects.filter(estado='pendiente').count()
if pendientes > 100:
    print(f"⚠️ ALERTA: {pendientes} correos pendientes en cola")
    # Aquí enviar email de alerta al admin
EOF
```

---

## 📋 CHECKLIST RÁPIDO

- [ ] Migración aplicada (`python manage.py migrate anuncios 0018`)
- [ ] Script de verificación pasó 100% (`python verificar_cola_correos.py`)
- [ ] Monitor web accesible (`/seguridad/cola-correos/`)
- [ ] Admin visible (`/admin/anuncios/colacorreos/`)
- [ ] Test de empleado completado
- [ ] Procesamiento automático configurado (Cron/Celery/APScheduler)
- [ ] Links en dashboard visible
- [ ] SMTP configurado en `/seguridad/configuracion/`

---

## 🆘 PROBLEMAS COMUNES

### "Migration 0018 not found"
```bash
# Verificar que existe
ls portal/migrations/0018_*.py

# Si no existe, actualizar repo
git pull origin main
```

### "Table cola_correos doesn't exist"
```bash
# Ejecutar migración
python manage.py migrate anuncios 0018

# Verificar
python manage.py migrate anuncios --plan
```

### "Permission denied" en monitor
```bash
# Verificar que usuario es admin
python manage.py shell
>>> from portal.models import UsuariosDelSistema
>>> u = UsuariosDelSistema.objects.filter(rol='admin').first()
>>> print(u)
```

### "Correos no se envían"
```bash
# 1. Ver si hay pendientes
python manage.py shell
>>> from portal.models import ColaCorreos
>>> ColaCorreos.objects.filter(estado='pendiente').count()

# 2. Procesar manualmente
python manage.py procesar_cola_correos --limite 10

# 3. Ver errores
>>> ColaCorreos.objects.filter(estado='error').values('mensaje_error').first()
```

---

## 📞 DOCUMENTACIÓN DE REFERENCIA

| Documento | Contenido |
|-----------|----------|
| `DOCUMENTACION_COLA_CORREOS.md` | Documentación técnica completa |
| `SETUP_COLA_CORREOS.md` | Guía rápida de 5 pasos |
| `DIAGRAMA_COLA_CORREOS.md` | Diagramas visuales del sistema |
| `RESUMEN_IMPLEMENTACION_COLA_CORREOS.md` | Resumen de lo implementado |
| `CHECKLIST_COLA_CORREOS.md` | Checklist de completitud |

---

## 💡 TIPS ÚTILES

**Ver estado actual:**
```bash
python manage.py shell
>>> from portal.models import ColaCorreos
>>> from django.utils import timezone
>>> 
>>> # Correos de hoy
>>> inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
>>> ColaCorreos.objects.filter(estado='enviado', fecha_envio__gte=inicio).count()
1500

>>> # Correos pendientes
>>> ColaCorreos.objects.filter(estado='pendiente').count()
45

>>> # Correos con error
>>> ColaCorreos.objects.filter(estado='error').count()
5
```

**Procesar cola con límite menor (para testing):**
```bash
python manage.py procesar_cola_correos --limite 10
```

**Limpiar cola de correos antiguos (mes a mes):**
```bash
python manage.py shell
>>> from portal.models import ColaCorreos
>>> from datetime import timedelta
>>> from django.utils import timezone
>>> 
>>> fecha_limite = timezone.now() - timedelta(days=30)
>>> ColaCorreos.objects.filter(
...     fecha_creacion__lt=fecha_limite,
...     estado='enviado'
... ).delete()
```

---

## ✅ VALIDACIÓN FINAL

Una vez completados todos los pasos, tu sistema estará:

```
✅ Base de datos migrada
✅ Modelo ColaCorreos funcional
✅ Vistas y URLs operacionales
✅ Admin interface disponible
✅ Monitor web accesible
✅ API JSON lista
✅ Management command listo
✅ Automatización configurada
✅ Pruebas pasadas
✅ Documentación disponible
✅ READY FOR PRODUCTION
```

---

## 📝 PRÓXIMA REUNIÓN

Discutir con equipo:
1. ¿Qué opción de automatización usar? (Cron/Celery/APScheduler)
2. ¿Configurar alertas si cola crece?
3. ¿Limpiar cola mensualmente de correos antiguos?
4. ¿Entrenaral equipo en uso del monitor?
5. ¿Monitoreo en tiempo real con Grafana? (opcional)

---

**¡El sistema está listo para ser desplegado!**

Próxima acción: `python manage.py migrate anuncios 0018`

