# Sistema de Cola de Correos - ITAVU

## Descripción General

El Sistema de Cola de Correos es un componente crítico de la aplicación ITAVU que gestiona el envío de correos electrónicos con respeto al límite diario de **2,000 correos** impuesto por el servidor de correos del gobierno.

## Características

✅ **Persistencia**: Todos los correos se almacenan en la base de datos  
✅ **Límite Diario**: Respeta máximo 2,000 correos por día  
✅ **Reintentos**: Hasta 3 intentos automáticos por correo fallido  
✅ **Fallback**: Si SMTP falla, los correos se guardan en la cola  
✅ **Auditoría**: Tracking completo de intentos, errores y fechas  
✅ **Interfaz Admin**: Panel para monitorear y gestionar la cola  
✅ **API JSON**: Endpoints para obtener estadísticas  

## Arquitectura

### Modelo: ColaCorreos

```python
class ColaCorreos(models.Model):
    TIPOS_CORREO_CHOICES = [
        ('bienvenida', 'Bienvenida'),
        ('recuperacion', 'Recuperación de Contraseña'),
        ('credenciales', 'Envío de Credenciales'),
        ('contacto', 'Contacto/Consulta'),
        ('otro', 'Otro'),
    ]
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('error', 'Error'),
    ]
    
    id_cola = models.AutoField(primary_key=True)
    tipo_correo = models.CharField(max_length=20, choices=TIPOS_CORREO_CHOICES)
    email_destino = models.EmailField()
    asunto = models.CharField(max_length=255)
    contenido_texto = models.TextField()
    contenido_html = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    mensaje_error = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    numero_intentos = models.IntegerField(default=0)
    id_empleado = models.ForeignKey(PersonalEmpleados, on_delete=models.SET_NULL, null=True, blank=True)
```

### Funciones Principales

#### 1. `guardar_correo_en_cola()`
Guarda un correo en la cola sin intentar enviarlo.

```python
from portal.email_utils import guardar_correo_en_cola

correo = guardar_correo_en_cola(
    tipo_correo='bienvenida',
    email_destino='usuario@example.com',
    asunto='Bienvenido a ITAVU',
    contenido_texto='Texto plano del correo',
    contenido_html='<p>HTML del correo</p>',
    id_empleado=None  # Opcional
)
```

#### 2. `enviar_correo_directo()`
Intenta enviar un correo vía SMTP. Si falla, lo guarda en la cola automáticamente.

```python
from portal.email_utils import enviar_correo_directo

success = enviar_correo_directo(
    email_destino='usuario@example.com',
    asunto='Asunto del correo',
    contenido_texto='Texto plano',
    contenido_html='<p>HTML</p>'
)
```

#### 3. `procesar_cola_correos(limite_diario=2000)`
Procesa los correos pendientes en la cola, respetando el límite diario.

```python
from portal.email_utils import procesar_cola_correos

resultado = procesar_cola_correos(limite_diario=2000)
print(f"Enviados: {resultado['enviados']}")
print(f"Errores: {resultado['errores']}")
print(f"Pendientes: {resultado['pendientes']}")
```

**Devuelve:**
```python
{
    'enviados': 150,      # Correos enviados exitosamente
    'errores': 5,         # Correos con error permanente
    'pendientes': 45      # Correos aún por enviar
}
```

## Uso

### 1. Aplicar Migración

```bash
python manage.py migrate anuncios 0018
```

Verifica que la tabla `cola_correos` se creó:
```bash
python manage.py dbshell
> SELECT COUNT(*) FROM cola_correos;
```

### 2. Procesar Cola Manualmente

**Comando de Management:**
```bash
python manage.py procesar_cola_correos --limite 2000
```

**Salida esperada:**
```
Procesando cola de correos...
Correos enviados: 150
Correos con error: 5
Correos pendientes: 45
```

### 3. Acceder al Monitor

**URL:** `http://localhost:8000/seguridad/cola-correos/`

El monitor muestra:
- Total de correos en la cola
- Correos pendientes
- Correos enviados hoy vs. límite (2000)
- Correos con error
- Tabla con últimos 20 correos

### 4. Procesar Desde el Panel

1. Ir a `/seguridad/cola-correos/`
2. Hacer clic en botón **"Procesar Cola Ahora"**
3. Ver resultados en modal popup

### 5. Admin Django

**URL:** `http://localhost:8000/admin/anuncios/colacorreos/`

Características:
- Filtrar por estado (Pendiente, Enviado, Error)
- Filtrar por tipo de correo
- Filtrar por fecha
- Ver detalles de errores
- Búsqueda por email o asunto
- Readonly para auditoría (no se pueden editar históricos)

## API Endpoints

### 1. Obtener Estadísticas

**URL:** `GET /api/estadisticas-cola/`

**Autenticación:** Requerida (admin)

**Respuesta:**
```json
{
  "success": true,
  "total": 500,
  "pendientes": 45,
  "enviados": 450,
  "errores": 5,
  "enviados_hoy": 1500,
  "limite_diario": 2000,
  "porcentaje_diario": 75.0,
  "por_tipo": {
    "Bienvenida": 200,
    "Credenciales": 150,
    "Recuperación": 100,
    "Contacto": 50
  }
}
```

### 2. Procesar Cola

**URL:** `POST /seguridad/cola-correos/procesar/`

**Autenticación:** Requerida (admin)

**Respuesta:**
```json
{
  "success": true,
  "enviados": 150,
  "errores": 5,
  "pendientes": 45,
  "message": "Procesamiento completado. Enviados: 150, Errores: 5"
}
```

## Flujo de Procesamiento

### Cuando se crea/edita un empleado con credenciales:

```
1. Usuario crea/edita empleado con usuario y contraseña
2. Sistema llama a enviar_correo_bienvenida_credenciales()
3. Esta función llama a enviar_correo_directo()
4. enviar_correo_directo() intenta enviar vía SMTP
   ├─ ✓ Si éxito → Guarda en cola con estado='enviado'
   └─ ✗ Si fallo → Guarda en cola con estado='pendiente' (para reintentar)
5. Usuario ve confirmación en pantalla
6. Correo se procesa cuando:
   ├─ Se ejecuta management command
   ├─ Se hace clic en "Procesar Cola Ahora" en admin
   └─ Se ejecuta procesamiento automático (ver Automatización)
```

### Cuando se intenta procesar la cola:

```
1. Calcular correos enviados hoy
   disponibles = 2000 - enviados_hoy

2. Si disponibles <= 0:
   └─ Esperar a mañana, no procesar más

3. Si disponibles > 0:
   ├─ Obtener correos pendientes (estado='pendiente', intentos < 3)
   ├─ Procesar hasta alcanzar disponibles
   ├─ Para cada correo:
   │  ├─ Intentar envío SMTP
   │  ├─ Si ✓: estado='enviado', fecha_envio=ahora
   │  └─ Si ✗: numero_intentos++
   │           Si numero_intentos >= 3: estado='error'
   │           Sino: Seguir pendiente para próximo ciclo
   └─ Retornar estadísticas
```

## Automatización (Opcional)

Para procesar la cola automáticamente cada X minutos, hay varias opciones:

### Opción 1: Cron Job (Recomendado)

**Linux/Mac:**
```bash
crontab -e

# Procesar cola cada 5 minutos
*/5 * * * * cd /ruta/al/proyecto && python manage.py procesar_cola_correos --limite 2000 >> /tmp/cola_correos.log 2>&1
```

**Windows - Task Scheduler:**
```batch
# Crear una tarea que ejecute cada 5 minutos
schtasks /create /tn "ITAVU_Cola_Correos" /tr "python C:\ruta\manage.py procesar_cola_correos" /sc minute /mo 5
```

### Opción 2: Celery (Para aplicaciones más grandes)

```bash
pip install celery redis
```

**portal/tasks.py:**
```python
from celery import shared_task
from .email_utils import procesar_cola_correos

@shared_task
def procesar_cola_correos_task():
    resultado = procesar_cola_correos(limite_diario=2000)
    return resultado
```

**core/celery.py:**
```python
from celery.schedules import crontab

app.conf.beat_schedule = {
    'procesar_cola_correos': {
        'task': 'portal.tasks.procesar_cola_correos_task',
        'schedule': crontab(minute='*/5'),  # Cada 5 minutos
    },
}
```

### Opción 3: APScheduler

```bash
pip install apscheduler
```

**core/apps.py:**
```python
from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig

def procesar_cola_job():
    from portal.email_utils import procesar_cola_correos
    procesar_cola_correos(limite_diario=2000)

class CoreConfig(AppConfig):
    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(procesar_cola_job, 'interval', minutes=5)
        scheduler.start()
```

## Verificación del Sistema

Ejecutar script de prueba:

```bash
python verificar_cola_correos.py
```

Pruebas realizadas:
- ✓ Verificación del modelo
- ✓ Guardado de correos
- ✓ Límite diario
- ✓ Estadísticas
- ✓ Procesamiento
- ✓ Reintentos
- ✓ Comando de management

## Monitoreo

### Ver correos en error:

```bash
python manage.py shell
>>> from portal.models import ColaCorreos
>>> ColaCorreos.objects.filter(estado='error').values('email_destino', 'mensaje_error')
```

### Ver correos pendientes:

```bash
>>> ColaCorreos.objects.filter(estado='pendiente').count()
45  # Hay 45 correos por enviar
```

### Ver correos de hoy:

```bash
>>> from django.utils import timezone
>>> inicio = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
>>> ColaCorreos.objects.filter(estado='enviado', fecha_envio__gte=inicio).count()
1500  # 1500 de 2000 enviados hoy
```

## Troubleshooting

### ❌ Problema: "Migration 0018 not found"

```bash
# Asegúrate de que migración existe
ls portal/migrations/0018_*.py

# Si no existe, verifica git
git status
git add portal/migrations/0018_*.py
```

### ❌ Problema: "Table cola_correos doesn't exist"

```bash
# Ejecutar migración
python manage.py migrate anuncios 0018

# Verificar
python manage.py migrate anuncios --plan
```

### ❌ Problema: "Correos no se están enviando"

```bash
# 1. Ver si hay correos pendientes
python manage.py shell
>>> from portal.models import ColaCorreos
>>> ColaCorreos.objects.filter(estado='pendiente').count()

# 2. Procesar manualmente
python manage.py procesar_cola_correos --limite 10

# 3. Ver errores
>>> ColaCorreos.objects.filter(estado='error').values('mensaje_error')
```

### ❌ Problema: "Se alcanzó límite de 2000 correos"

```bash
# Esperar a siguiente día (resetea en medianoche)
# O procesar parcialmente con --limite menor
python manage.py procesar_cola_correos --limite 100
```

## Logs

Los correos se registran en:
- **Tabla:** `cola_correos`
- **Campos de auditoría:**
  - `fecha_creacion` - Cuándo se generó el correo
  - `fecha_envio` - Cuándo se intentó enviar
  - `numero_intentos` - Número de intentos
  - `mensaje_error` - Último mensaje de error
  - `estado` - Estado actual (pendiente, enviado, error)

## Performance

Para optimizar con muchos correos:

```python
# Agregar índices en settings.py
DATABASES = {
    'default': {
        ...
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

# Limpiar correos antiguos cada mes
from django.utils import timezone
from datetime import timedelta
from portal.models import ColaCorreos

tres_meses_atras = timezone.now() - timedelta(days=90)
ColaCorreos.objects.filter(
    fecha_creacion__lt=tres_meses_atras,
    estado='enviado'
).delete()
```

## Seguridad

- ✅ Solo admins pueden acceder al monitor
- ✅ URLs protegidas con `@login_required`
- ✅ Permiso verificado con `_usuario_es_admin_sistema()`
- ✅ CSRF token requerido en POST requests
- ✅ Campos readonly en admin para auditoría
- ✅ Contraseñas nunca se guardan en cola (solo en histórico temporal)

## Soporte

Para problemas o preguntas sobre el sistema de cola de correos:

1. Revisar `/admin/anuncios/colacorreos/` para ver estado
2. Ejecutar `python verificar_cola_correos.py`
3. Revisar logs en tabla `cola_correos`
4. Ejecutar `python manage.py procesar_cola_correos --limite 10` para debug

---

**Última actualización:** 2024  
**Versión:** 1.0  
**Status:** Producción ✓

