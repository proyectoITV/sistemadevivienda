# SETUP RÁPIDO - Sistema de Cola de Correos

## 🚀 Pasos de Implementación

### 1. Aplicar Migración (PRIMERO)

```bash
cd c:\xampp\htdocs\Desarrollos\ web\sistemadevivienda
python manage.py migrate anuncios 0018
```

**Verificar:**
```bash
python manage.py dbshell
SELECT COUNT(*) FROM cola_correos;
# Debe retornar 0 (tabla vacía)
```

### 2. Ejecutar Script de Verificación

```bash
python verificar_cola_correos.py
```

**Salida esperada:** ✓ TODAS LAS PRUEBAS PASARON

### 3. Acceder al Monitor Web

- **URL:** http://localhost:8000/seguridad/cola-correos/
- **Usuario:** Admin del sistema
- **Funcionalidad:** Ver estado de correos, procesar cola manualmente

### 4. Acceder al Admin Django

- **URL:** http://localhost:8000/admin/anuncios/colacorreos/
- **Funcionalidad:** Filtrar, buscar, ver detalles de correos

### 5. Probar Envío de Credenciales

```bash
# 1. Ir a /empleados/crear/
# 2. Crear empleado con usuario y correo
# 3. El sistema enviará credenciales
# 4. Revisar en monitor /seguridad/cola-correos/
```

## 📊 Verificaciones Rápidas

### Ver correos pendientes

```bash
python manage.py shell
>>> from anuncios.models import ColaCorreos
>>> ColaCorreos.objects.filter(estado='pendiente').count()
```

### Procesar cola manualmente

```bash
python manage.py procesar_cola_correos --limite 2000
```

### Ver estadísticas

```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/estadisticas-cola/
```

## ⚙️ Configuración Recomendada

### Opción A: Cron Job (RECOMENDADO)

Crear archivo `/cron_cola_correos.bat` (Windows):

```batch
@echo off
cd C:\xampp\htdocs\Desarrollos\ web\sistemadevivienda
python manage.py procesar_cola_correos --limite 2000 >> C:\xampp\logs\cola_correos.log 2>&1
```

Agendar en Windows Task Scheduler:
- **Frecuencia:** Cada 5 minutos
- **Comando:** `C:\xampp\scripts\python.exe C:\cron_cola_correos.bat`
- **Ejecutar con privilegios:** Sí

### Opción B: Script Python en Background

```bash
# En terminal, dejar ejecutándose
while True:
    python manage.py procesar_cola_correos --limite 2000
    sleep(300)  # Esperar 5 minutos
```

## 🐛 Troubleshooting

| Problema | Solución |
|----------|----------|
| "Migration 0018 not found" | `git pull` o crear migración manualmente |
| "Table cola_correos doesn't exist" | `python manage.py migrate anuncios 0018` |
| "No permissions" | Verificar que usuario sea admin del sistema |
| Correos no se envían | Ejecutar `python manage.py procesar_cola_correos --limite 10` |
| Límite de 2000 alcanzado | Esperar hasta mañana o limpiar correos antiguos |

## 📝 Flujo de Trabajo Típico

1. **Usuario crea empleado** → Correo se guarda en cola
2. **Admin procesa cola** → Correos se envían (máx 2000/día)
3. **Si falla SMTP** → Correo permanece en cola
4. **Reintentos automáticos** → Hasta 3 intentos por correo
5. **Después de 3 fallos** → Se marca como error

## ✅ Checklist de Producción

- [ ] Migración aplicada (`python manage.py migrate anuncios 0018`)
- [ ] Script de verificación pasó (`python verificar_cola_correos.py`)
- [ ] Monitor accesible en `/seguridad/cola-correos/`
- [ ] Admin accesible en `/admin/anuncios/colacorreos/`
- [ ] Cron job configurado (procesamiento cada 5 min)
- [ ] Prueba de envío de credenciales realizada
- [ ] Logs configurados (opcional)
- [ ] Alertas configuradas si cola crece (opcional)

## 📞 Soporte

**Documentación completa:** `DOCUMENTACION_COLA_CORREOS.md`

**Archivos relacionados:**
- `anuncios/models.py` - Modelo ColaCorreos
- `anuncios/email_utils.py` - Funciones de queue
- `anuncios/management/commands/procesar_cola_correos.py` - Management command
- `anuncios/views.py` - Vistas del monitor
- `anuncios/templates/anuncios/seguridad/monitor_cola_correos.html` - Template

---

¿Necesitas ayuda con algún paso? Contacta al administrador del sistema.
