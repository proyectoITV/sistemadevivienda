# Diagrama del Sistema de Cola de Correos

## 1. Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────┐
│                     SISTEMA ITAVU - COLA DE CORREOS                 │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐
│  GENERACIÓN DE EMAIL │
│  - Crear Empleado    │
│  - Editar Empleado   │
│  - Credenciales      │
│  - Contacto Sitio    │
└─────────────┬────────┘
              │
              ▼
┌──────────────────────────────────────────┐
│  enviar_correo_directo()                 │
│  ├─ Obtener Config SMTP                  │
│  ├─ Intentar Envío                       │
│  └─ Fallback a Cola si Error             │
└─────────────┬────────────────────────────┘
              │
        ┌─────┴─────┐
        │           │
       ✓✓          ✗✗
        │           │
        ▼           ▼
    ┌───────┐  ┌─────────────┐
    │Enviado│  │ColaCorreos  │
    │(Hoy)  │  │(Pendiente)  │
    └───────┘  └─────────────┘
        │           │
        │           │ procesar_cola_correos()
        │           │ ├─ Calcular capacidad
        │           │ ├─ Obtener pendientes
        │           │ ├─ Intentar envío
        │           │ └─ Actualizar estado
        │           │
        │      ┌────┴────┐
        │      │          │
        │     ✓✓         ✗✗
        │      │          │
        │      ▼          ▼
        │  ┌───────┐  ┌──────┐
        │  │Enviado│  │Error │
        │  │       │  │(3int)│
        │  └───────┘  └──────┘
        │      │          │
        └──────┴──────────┘
               │
               ▼
        ┌────────────┐
        │ Monitor    │
        │ - Ver      │
        │ - Procesar │
        │ - Alertas  │
        └────────────┘
```

---

## 2. Modelo de Datos

```
┌─────────────────────────────────────┐
│        ColaCorreos (BD)             │
├─────────────────────────────────────┤
│ id_cola          INTEGER PK         │
│ tipo_correo      VARCHAR(20)        │
│ email_destino    EMAIL              │
│ asunto           VARCHAR(255)       │
│ contenido_texto  TEXT               │
│ contenido_html   TEXT               │
│ estado           VARCHAR(20)        │◄── Valores:
│ mensaje_error    TEXT (nullable)    │    - pendiente
│ fecha_creacion   DATETIME           │    - enviado
│ fecha_envio      DATETIME (nullable)│    - error
│ numero_intentos  INTEGER (0-3)      │
│ id_empleado      FK (nullable)      │
│                                     │
│ ÍNDICES:                            │
│ - (estado, fecha_creacion)          │
│ - (email_destino)                   │
└─────────────────────────────────────┘
```

---

## 3. Flujo de Procesamiento Diario

```
                          00:00 (Medianoche)
                          ┌─ Contador Diario = 0
                          │

    06:00 AM
    ┌─────────────────────┐
    │ Primer correo creado │────┐
    │ Usuario: admin@...   │    │ guardar_correo_en_cola()
    └─────────────────────┘    │ estado = 'pendiente'
                               │
                      ┌────────▼────────┐
                      │ procesar_cola() │
                      │ - disponibles: 2000
                      │ - procesa correo
                      │ - estado = 'enviado'
                      │ Enviados hoy: 1
                      └────────┬────────┘
                               │
    ...más correos durante el día...
    
    20:00 (8 PM)
    Enviados hoy: 1999
    Disponibles: 1
    
    20:15
    Nuevo correo creado
    │
    ├─ procesar_cola()
    │  - disponibles: 1
    │  - procesa 1 correo
    │  - Enviados hoy: 2000
    │  - ✓ LÍMITE ALCANZADO
    │
    └─ Próximos correos quedan PENDIENTES
       hasta mañana
    
    23:59:59
    │
    └─ CONTADOR = 2000 (máximo)
       Correos pendientes: 45
       Estado: esperando mañana
    
    00:00:00 (Medianoche - Nuevo día)
    │
    ├─ CONTADOR RESETEA a 0
    ├─ Correos pendientes: 45 (se mantienen)
    │
    └─ procesar_cola() puede ejecutar de nuevo
       disponibles = 2000 - 0 = 2000
       Procesa los 45 pendientes + nuevos
```

---

## 4. Máquina de Estados

```
                    ┌─────────────┐
                    │   CREADO    │
                    │ (nuevo correo)
                    └──────┬──────┘
                           │
                ┌──────────┼──────────┐
                │                     │
                ▼                     ▼
         ┌────────────┐        ┌────────────┐
         │INTENTAR    │        │GUARDAR EN  │
         │ENVÍO SMTP  │        │COLA        │
         └────┬───────┘        │(pendiente) │
              │                └────────────┘
         ┌────┴────┐                │
         │          │               │
        ✓✓         ✗✗              │
         │          │               │
         ▼          ▼               │
    ┌─────────┐ ┌────────┐         │
    │ENVIADO  │ │GUARDAR │◄────────┘
    │HOYSMTP) │ │PENDIENTE
    │         │ │        │
    └─────────┘ └────┬───┘
         │            │
         │    procesar_cola()
         │    invoca reintentos
         │            │
         │      ┌─────┴─────┐
         │      │            │
         │     ✓✓           ✗✗
         │      │            │
         │      ▼            ▼
         │  ┌────────┐  ┌─────────────┐
         │  │ENVIADO │  │número_int++│
         │  │        │  │intentos<3?  │
         │  └────────┘  │            │
         │              └──┬─────┬───┘
         │                 │     │
         │                ✓✓    ✗✗
         │                 │     │
         │                 ▼     ▼
         │            ┌────────┐ ┌────────┐
         │            │Pendiente│ │ERROR   │
         │            │(reintentar)│(3 int)│
         │            └────────┘ └────────┘
         │
         └─────────────────────────┘
                   │
                   ▼
            [FIN - Histórico en BD]
```

---

## 5. Ciclo de Procesamiento

```
procesar_cola_correos(limite_diario=2000)
│
├─ FASE 1: CÁLCULO DE CAPACIDAD
│  ├─ inicio_dia = HOY 00:00:00
│  ├─ enviados_hoy = COUNT(estado='enviado' AND fecha_envio >= hoy)
│  └─ disponibles = 2000 - enviados_hoy
│     │
│     └─ ¿disponibles > 0?
│        │
│        ├─ NO  ──► RETURN {enviados: 0, errores: 0, pendientes: X}
│        │
│        └─ SÍ  ──► Continuar
│
├─ FASE 2: OBTENER CORREOS A PROCESAR
│  ├─ Query: estado='pendiente' AND numero_intentos < 3
│  ├─ Order by: fecha_creacion (más antiguos primero)
│  ├─ Limit: disponibles
│  └─ Resultados: correos_pendientes[]
│
├─ FASE 3: PROCESAR CADA CORREO
│  │
│  ├─► FOR EACH correo IN correos_pendientes:
│  │   │
│  │   ├─ Obtener config SMTP
│  │   ├─ Intentar envío
│  │   │  │
│  │   │  ├─ ✓ ÉXITO
│  │   │  │  ├─ estado = 'enviado'
│  │   │  │  ├─ fecha_envio = AHORA
│  │   │  │  ├─ numero_intentos++
│  │   │  │  └─ SAVE()
│  │   │  │
│  │   │  └─ ✗ ERROR
│  │   │     ├─ numero_intentos++
│  │   │     ├─ mensaje_error = str(error)
│  │   │     │
│  │   │     └─ ¿numero_intentos >= 3?
│  │   │        │
│  │   │        ├─ SÍ
│  │   │        │  ├─ estado = 'error'
│  │   │        │  └─ SAVE()
│  │   │        │
│  │   │        └─ NO
│  │   │           ├─ estado = 'pendiente' (se mantiene)
│  │   │           └─ SAVE() para próximo ciclo
│  │   │
│  │   └─ Continuar con siguiente correo
│  │
│  └─ CONTADORES:
│     ├─ enviados_count = COUNT(estado='enviado')
│     ├─ errores_count = COUNT(estado='error' AND numero_intentos >= 3)
│     └─ pendientes_count = COUNT(estado='pendiente')
│
└─ FASE 4: RETORNAR RESULTADOS
   └─ RETURN {
       'enviados': enviados_count,
       'errores': errores_count,
       'pendientes': pendientes_count
      }
```

---

## 6. Vista de Interacción Web

```
╔════════════════════════════════════════════════════════════════╗
║               Monitor de Cola de Correos                       ║
║            http://localhost:8000/seguridad/cola-correos/       ║
╚════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────┐
│ ESTADÍSTICAS                                                 │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐          │
│  │Total        │  │Pendientes   │  │Enviados Hoy  │          │
│  │500 correos  │  │45 correos   │  │1500 / 2000   │          │
│  └─────────────┘  └─────────────┘  │ [█████████   │          │
│                                     │  75%]        │          │
│  ┌─────────────┐                    └──────────────┘          │
│  │Errores      │                                               │
│  │5 correos    │                                               │
│  └─────────────┘                                               │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ACCIONES                                                     │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  [▶ Procesar Cola Ahora]  [↻ Actualizar]  [⚙ Configuración] │
│                                                               │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ ÚLTIMOS CORREOS                                              │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│ Email         │ Tipo        │ Estado    │ Int. │ Fecha      │
├───────────────┼─────────────┼───────────┼─────┼────────────┤
│user@itavu.gob │ Bienvenida  │ ✓ Enviado │ 1/3 │ 22/11 10:5 │
│admin@itavu... │ Credenciales│ ⏱ Pendien │ 1/3 │ 22/11 10:4 │
│test@mail.com  │ Contacto    │ ✗ Error   │ 3/3 │ 22/11 09:2 │
│...            │ ...         │ ...       │ ... │ ...        │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 7. URLs y Endpoints

```
VISTAS WEB
├─ /seguridad/cola-correos/
│  └─ GET: Ver monitor (template HTML)
│     Requiere: Login + Admin
│
├─ /seguridad/cola-correos/procesar/
│  └─ POST: Procesar cola (JSON response)
│     Requiere: Login + Admin + CSRF Token
│     Response: {success, enviados, errores, pendientes}
│
└─ /api/estadisticas-cola/
   └─ GET: Obtener estadísticas (JSON)
      Requiere: Login + Admin
      Response: {total, pendientes, enviados, errores, etc}

ADMIN
└─ /admin/anuncios/colacorreos/
   ├─ List: Ver todos los correos
   ├─ Filter: Por estado, tipo, fecha
   ├─ Search: Por email, asunto
   └─ Details: Ver detalles (readonly)
```

---

## 8. Flujo Completo: Crear Empleado

```
1. Usuario Admin
   └─ Va a /empleados/crear/

2. Rellena Formulario
   ├─ Nombre: "Juan García"
   ├─ Usuario: "jgarcia"
   ├─ Contraseña: "123456"
   ├─ Email: "juan@itavu.gob"
   └─ Otros campos...

3. Click: [Guardar]
   │
   ▼ Vista: crear_empleado()
   ├─ Valida formulario
   ├─ Hash contraseña
   ├─ Guarda PersonalEmpleados
   └─ ¿usuario + email?
      │
      ├─ SÍ ──► enviar_correo_bienvenida_credenciales()
      │         │
      │         ▼ email_utils.py
      │         enviar_correo_directo(
      │           email_destino="juan@itavu.gob",
      │           asunto="Bienvenido a ITAVU",
      │           html="<p>Tu contraseña es...</p>"
      │         )
      │         │
      │         ├─ Intenta SMTP
      │         │
      │         ├─ ✓ Éxito
      │         │  └─ guardar_correo_en_cola(estado='enviado')
      │         │
      │         └─ ✗ Fallo
      │            └─ guardar_correo_en_cola(estado='pendiente')
      │
      └─ NO ──► Sin correo

4. Usuario ve confirmación
   "✓ Empleado creado. Credenciales enviadas a juan@itavu.gob"

5. Admin ve en Monitor
   └─ /seguridad/cola-correos/
      ├─ Total: 1
      ├─ Pendientes: 1 (si SMTP falló)
      └─ Click: [Procesar Cola Ahora]
         └─ Se intenta envío SMTP nuevamente
            ├─ ✓ Éxito: estado='enviado'
            └─ ✗ Fallo: reintentar después
```

---

## 9. Estadísticas en Tiempo Real

```
API Endpoint: /api/estadisticas-cola/

RESPUESTA:
{
  "success": true,
  "total": 500,                    ◄── Todos los correos en cola
  "pendientes": 45,                ◄── Esperando envío
  "enviados": 450,                 ◄── Enviados exitosamente
  "errores": 5,                    ◄── Con error permanente
  "enviados_hoy": 1500,            ◄── Desde las 00:00
  "limite_diario": 2000,           ◄── Máximo permitido
  "porcentaje_diario": 75.0,       ◄── 1500/2000 * 100
  "por_tipo": {
    "Bienvenida": 200,
    "Credenciales": 150,
    "Recuperación": 100,
    "Contacto": 50
  }
}
```

---

## 10. Ciclo de Reintentos

```
Correo fallido después de 1er intento:
│
├─ Intento 1 (10:00 AM)
│  └─ ✗ Error SMTP timeout
│     estado = pendiente
│     numero_intentos = 1
│
├─ Intento 2 (10:05 AM - próximo ciclo)
│  └─ ✗ Error connection refused
│     estado = pendiente
│     numero_intentos = 2
│
├─ Intento 3 (10:10 AM - próximo ciclo)
│  └─ ✗ Error authentication failed
│     estado = ERROR
│     numero_intentos = 3
│     mensaje_error = "Authentication failed after 3 attempts"
│
└─ ✗ PARADO - No habrá más reintentos
   Admin debe investigar configuración SMTP
```

---

**Notas Visuales:**
- ✓✓ = Éxito
- ✗✗ = Fallo
- ⏱ = Pendiente
- █ = Porcentaje usado
- → = Flujo de datos
- ▼ = Progresión temporal
