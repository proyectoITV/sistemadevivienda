import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.template.loader import render_to_string
from .models import ConfiguracionSistema, ColaCorreos
from django.utils import timezone
from django.db.models import Q


def obtener_configuracion_smtp():
	"""Obtiene la configuración SMTP del sistema."""
	try:
		return ConfiguracionSistema.objects.first()
	except Exception:
		return None


def guardar_correo_en_cola(tipo_correo, email_destino, asunto, contenido_texto, contenido_html, id_empleado=None):
	"""
	Guarda un correo en la cola para envío posterior.
	
	Args:
		tipo_correo: Tipo de correo (bienvenida, recuperacion, credenciales, contacto, otro)
		email_destino: Email destino
		asunto: Asunto del correo
		contenido_texto: Contenido en texto plano
		contenido_html: Contenido en HTML
		id_empleado: ID del empleado (opcional)
		
	Returns:
		ColaCorreos: Instancia creada
	"""
	try:
		cola = ColaCorreos.objects.create(
			tipo_correo=tipo_correo,
			email_destino=email_destino,
			asunto=asunto,
			contenido_texto=contenido_texto,
			contenido_html=contenido_html,
			id_empleado_id=id_empleado,
			estado='pendiente'
		)
		print(f"✓ Correo guardado en cola: {email_destino} (ID: {cola.id_cola})")
		return cola
	except Exception as e:
		print(f"✗ Error al guardar correo en cola: {str(e)}")
		return None


def enviar_correo_directo(email_destino, asunto, contenido_texto, contenido_html):
	"""
	Intenta enviar un correo directamente. Si falla, lo guarda en la cola.
	
	Args:
		email_destino: Email destino
		asunto: Asunto del correo
		contenido_texto: Contenido en texto plano
		contenido_html: Contenido en HTML
		
	Returns:
		bool: True si se envió, False si se guardó en cola
	"""
	config = obtener_configuracion_smtp()
	
	if not config or not config.smtp_host:
		print("⚠ Configuración SMTP no disponible - guardando en cola")
		guardar_correo_en_cola('otro', email_destino, asunto, contenido_texto, contenido_html)
		return False
	
	try:
		# Crear mensaje
		message = MIMEMultipart('alternative')
		message['Subject'] = asunto
		message['From'] = config.email_desde or config.smtp_usuario
		message['To'] = email_destino
		
		# Adjuntar versión texto plano
		text_part = MIMEText(contenido_texto, 'plain', 'utf-8')
		message.attach(text_part)
		
		# Adjuntar versión HTML
		html_part = MIMEText(contenido_html, 'html', 'utf-8')
		message.attach(html_part)
		
		# Conectar al servidor SMTP y enviar
		with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=10) as server:
			if config.smtp_usar_tls:
				server.starttls()
			
			if config.smtp_usuario and config.smtp_contrasena:
				server.login(config.smtp_usuario, config.smtp_contrasena)
			
			server.send_message(message)
		
		print(f"✓ Correo enviado directamente a {email_destino}")
		return True
		
	except Exception as e:
		print(f"✗ Error al enviar correo directamente: {str(e)} - guardando en cola")
		guardar_correo_en_cola('otro', email_destino, asunto, contenido_texto, contenido_html)
		return False


def enviar_notificacion_mantenimiento(ticket, email_destino, titulo_evento, resumen, id_empleado=None, nombre_destinatario=None):
	"""Envía una notificación del módulo de mantenimiento al solicitante o a soporte."""
	if not email_destino:
		return False

	config = obtener_configuracion_smtp()
	nombre_corto = config.nombre_corto if config else 'Sistema'
	nombre_destinatario = nombre_destinatario or ticket.solicitante.nombre_completo
	asunto = f"[{nombre_corto}] Mantenimiento #{ticket.id_ticket_mantenimiento}: {titulo_evento}"
	contenido_texto = (
		f"Hola {nombre_destinatario},\n\n"
		f"Tu ticket de mantenimiento #{ticket.id_ticket_mantenimiento} ({ticket.asunto}) tuvo una actualización.\n\n"
		f"Estado actual: {ticket.get_estado_display()}\n"
		f"Equipo: {ticket.equipo or ticket.get_tipo_equipo_display()}\n"
		f"Resumen: {resumen}\n\n"
		f"Departamento solicitante: {ticket.departamento_solicitante.departamento if ticket.departamento_solicitante else 'No definido'}\n"
		f"Departamento de soporte: {ticket.departamento_soporte.departamento}\n"
	)
	contenido_html = f"""
		<div style=\"font-family: Arial, sans-serif; color: #243447;\">
			<h2 style=\"color:#ab0033;\">Servicio de Mantenimiento</h2>
			<p>Hola <strong>{nombre_destinatario}</strong>,</p>
			<p>Tu ticket <strong>#{ticket.id_ticket_mantenimiento}</strong> tuvo una actualización.</p>
			<ul>
				<li><strong>Asunto:</strong> {ticket.asunto}</li>
				<li><strong>Estado actual:</strong> {ticket.get_estado_display()}</li>
				<li><strong>Equipo:</strong> {ticket.equipo or ticket.get_tipo_equipo_display()}</li>
				<li><strong>Resumen:</strong> {resumen}</li>
			</ul>
			<p>Si necesitas más información, entra al módulo de Servicio de Mantenimiento en el sistema.</p>
		</div>
	"""
	return enviar_correo_directo(email_destino, asunto, contenido_texto, contenido_html)


def procesar_cola_correos(limite_diario=2000):
	"""
	Procesa la cola de correos pendientes.
	Respeta el límite diario configurado.
	
	Args:
		limite_diario: Límite de correos a enviar por día (default: 2000)
		
	Returns:
		dict: Estadísticas de envío {enviados, errores, pendientes}
	"""
	config = obtener_configuracion_smtp()
	
	if not config or not config.smtp_host:
		print("⚠ Configuración SMTP no disponible")
		return {'enviados': 0, 'errores': 0, 'pendientes': 0}
	
	from datetime import datetime, timedelta
	
	# Obtener correos enviados hoy
	inicio_dia = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
	enviados_hoy = ColaCorreos.objects.filter(
		estado='enviado',
		fecha_envio__gte=inicio_dia
	).count()
	
	# Calcular cuántos correos aún podemos enviar
	correos_disponibles = limite_diario - enviados_hoy
	
	if correos_disponibles <= 0:
		print(f"⚠ Límite diario alcanzado ({limite_diario} correos)")
		return {'enviados': 0, 'errores': 0, 'pendientes': ColaCorreos.objects.filter(estado='pendiente').count()}
	
	# Obtener correos pendientes (intentar 3 veces máximo)
	correos_pendientes = ColaCorreos.objects.filter(
		estado='pendiente',
		numero_intentos__lt=3
	).order_by('fecha_creacion')[:correos_disponibles]
	
	enviados = 0
	errores = 0
	
	for correo in correos_pendientes:
		try:
			# Crear mensaje
			message = MIMEMultipart('alternative')
			message['Subject'] = correo.asunto
			message['From'] = config.email_desde or config.smtp_usuario
			message['To'] = correo.email_destino
			
			# Adjuntar versión texto plano
			text_part = MIMEText(correo.contenido_texto, 'plain', 'utf-8')
			message.attach(text_part)
			
			# Adjuntar versión HTML
			html_part = MIMEText(correo.contenido_html, 'html', 'utf-8')
			message.attach(html_part)
			
			# Conectar al servidor SMTP y enviar
			with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=10) as server:
				if config.smtp_usar_tls:
					server.starttls()
				
				if config.smtp_usuario and config.smtp_contrasena:
					server.login(config.smtp_usuario, config.smtp_contrasena)
				
				server.send_message(message)
			
			# Marcar como enviado
			correo.estado = 'enviado'
			correo.fecha_envio = timezone.now()
			correo.numero_intentos += 1
			correo.save()
			
			print(f"✓ Correo enviado desde cola a {correo.email_destino}")
			enviados += 1
			
		except Exception as e:
			error_msg = str(e)[:500]  # Limitar longitud del mensaje
			correo.numero_intentos += 1
			
			# Si ya intentó 3 veces, marcar como error
			if correo.numero_intentos >= 3:
				correo.estado = 'error'
				correo.mensaje_error = f"Error después de 3 intentos: {error_msg}"
				print(f"✗ Correo marcado como error (3 intentos): {correo.email_destino}")
				errores += 1
			else:
				correo.mensaje_error = error_msg
				print(f"✗ Error al enviar a {correo.email_destino} (intento {correo.numero_intentos})")
			
			correo.save()
	
	pendientes = ColaCorreos.objects.filter(estado='pendiente').count()
	
	print(f"\n📊 Resumen de procesamiento de cola:")
	print(f"  - Enviados: {enviados}")
	print(f"  - Errores: {errores}")
	print(f"  - Pendientes: {pendientes}")
	print(f"  - Enviados hoy: {enviados_hoy + enviados}/{limite_diario}")
	
	return {'enviados': enviados, 'errores': errores, 'pendientes': pendientes}



def enviar_correo_contacto(contacto):
	"""
	Envía correo de confirmación al usuario después de recibir su mensaje.
	
	Args:
		contacto: Instancia de SeguridadContactanos
		
	Returns:
		bool: True si se envió correctamente, False en caso contrario
	"""
	config = obtener_configuracion_smtp()
	
	if not config or not config.smtp_host:
		print("⚠ Configuración SMTP no disponible")
		return False
	
	try:
		# Preparar contexto para la plantilla
		context = {
			'nombre': contacto.nombre_completo,
			'folio': str(contacto.uuid_folio),
			'asunto': contacto.asunto,
			'razon_social': config.razon_social,
		}
		
		# Renderizar HTML del correo
		html_message = render_to_string('desarrollo/web/email_confirmacion.html', context)
		
		# Crear mensaje
		message = MIMEMultipart('alternative')
		message['Subject'] = f"Confirmación de recepción - Folio: {contacto.uuid_folio}"
		message['From'] = config.email_desde or config.smtp_usuario
		message['To'] = contacto.email
		
		# Adjuntar versión texto plano
		text_message = MIMEText(f"""
Hola {contacto.nombre_completo},

Tu mensaje ha sido recibido correctamente por {config.razon_social}.

Folio de seguimiento: {contacto.uuid_folio}
Asunto: {contacto.asunto}

Puedes usar tu folio para dar seguimiento a tu mensaje en:
{context.get('url_seguimiento', 'https://tu-sitio.com/seguimiento/')}

Pronto nos pondremos en contacto contigo.

Saludos cordiales,
{config.razon_social}
		""".strip(), 'plain')
		message.attach(text_message)
		
		# Adjuntar versión HTML
		html_message_obj = MIMEText(html_message, 'html')
		message.attach(html_message_obj)
		
		# Conectar al servidor SMTP y enviar
		with smtplib.SMTP(config.smtp_host, config.smtp_port, timeout=10) as server:
			if config.smtp_usar_tls:
				server.starttls()
			
			if config.smtp_usuario and config.smtp_contrasena:
				server.login(config.smtp_usuario, config.smtp_contrasena)
				server.login(config.smtp_usuario, config.smtp_contrasena)
			
			server.send_message(message)
		
		print(f"✓ Correo enviado a {contacto.email}")
		return True
		
	except Exception as e:
		print(f"✗ Error al enviar correo: {str(e)}")
		return False

def enviar_correo_recuperacion(usuario, recuperacion):
	"""
	Envía correo para recuperar contraseña.
	
	Args:
		usuario: Instancia de PersonalEmpleados
		recuperacion: Instancia de RecuperacionContrasena
		
	Returns:
		bool: True si se envió correctamente, False en caso contrario
	"""
	from django.urls import reverse
	from django.conf import settings
	
	config = obtener_configuracion_smtp()
	
	if not config or not config.smtp_host:
		print("⚠ Configuración SMTP no disponible")
		return False
	
	try:
		# Construir URL de restablecimiento
		enlace_restablecimiento = f"{settings.SITE_URL}/restablecer-contrasena/{recuperacion.token}/"
		
		# Preparar contexto para la plantilla
		context = {
			'nombre': usuario.nombre_completo,
			'usuario': usuario.usuario,
			'enlace': enlace_restablecimiento,
			'razon_social': config.razon_social,
		}
		
		# Renderizar HTML del correo
		html_message = render_to_string('desarrollo/web/email_recuperacion.html', context)
		
		# Crear mensaje
		message = MIMEMultipart('alternative')
		message['Subject'] = "Recuperación de contraseña - ITAVU"
		message['From'] = config.email_desde or config.smtp_usuario
		message['To'] = usuario.email
		
		# Adjuntar versión texto plano
		text_part = MIMEText("Solicitud de recuperación de contraseña. Visita el enlace en el correo HTML para continuar.", 'plain', 'utf-8')
		message.attach(text_part)
		
		# Adjuntar versión HTML
		html_part = MIMEText(html_message, 'html', 'utf-8')
		message.attach(html_part)
		
		# Enviar correo
		with smtplib.SMTP(config.smtp_host, config.smtp_port) as server:
			if config.smtp_usar_tls:
				server.starttls()
			
			if config.smtp_usuario and config.smtp_contrasena:
				server.login(config.smtp_usuario, config.smtp_contrasena)
			
			server.send_message(message)
		
		print(f"✓ Correo de recuperación enviado a {usuario.email}")
		return True
		
	except Exception as e:
		print(f"✗ Error al enviar correo de recuperación: {str(e)}")
		return False


def enviar_correo_bienvenida_credenciales(empleado, password_texto_plano):
	"""
	Envía correo de bienvenida con credenciales de acceso al sistema.
	IMPORTANTE: Solo llamar cuando se configuran credenciales por primera vez.
	
	Args:
		empleado: Instancia de PersonalEmpleados
		password_texto_plano: Contraseña en texto plano (solo disponible al momento de crear/cambiar)
		
	Returns:
		bool: True si se envió correctamente, False en caso contrario
	"""
	config = obtener_configuracion_smtp()
	
	if not config or not config.smtp_host:
		print("⚠ Configuración SMTP no disponible")
		return False
	
	if not empleado.email:
		print("⚠ El empleado no tiene correo electrónico registrado")
		return False
	
	if not empleado.usuario or not password_texto_plano:
		print("⚠ No se puede enviar correo sin usuario o contraseña")
		return False
	
	from django.conf import settings
	
	# URL del sistema
	url_sistema = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
	url_login = f"{url_sistema}/login/"
	
	# Preparar contexto para la plantilla
	context = {
		'nombre': empleado.nombre_completo,
		'usuario': empleado.usuario,
		'password': password_texto_plano,
		'email': empleado.email,
		'url_login': url_login,
		'razon_social': config.razon_social,
		'nombre_corto': config.nombre_corto,
	}
	
	# Renderizar HTML del correo
	html_message = render_to_string('desarrollo/web/email_bienvenida_credenciales.html', context)
	
	# Crear mensaje de texto
	text_content = f"""
¡Bienvenido(a) al equipo {config.nombre_corto}!

Hola {empleado.nombre_completo},

Nos complace darte la bienvenida al Sistema de Vivienda {config.razon_social}.

TUS CREDENCIALES DE ACCESO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usuario: {empleado.usuario}
Contraseña: {password_texto_plano}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANTE - TEN CUIDADO CON TUS CREDENCIALES:
• Guarda esta información en un lugar seguro
• NO compartas tu contraseña con nadie
• Cambia tu contraseña periódicamente
• NO uses la misma contraseña en otros sistemas

Puedes acceder al sistema en:
{url_login}

Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.

Saludos cordiales,
Equipo {config.razon_social}
	""".strip()
	
	# Intentar enviar directo o guardar en cola
	return enviar_correo_directo(
		email_destino=empleado.email,
		asunto=f"Bienvenido al equipo {config.nombre_corto} - Tus credenciales de acceso",
		contenido_texto=text_content,
		contenido_html=html_message
	)


def enviar_credenciales_existentes(empleado):
	"""
	Genera una nueva contraseña temporal y la envía al correo del empleado.
	
	Args:
		empleado: Instancia de PersonalEmpleados
		
	Returns:
		tuple: (bool, str) - (éxito, contraseña_temporal)
	"""
	config = obtener_configuracion_smtp()
	
	if not config or not config.smtp_host:
		print("⚠ Configuración SMTP no disponible")
		return False, None
	
	if not empleado.email:
		print("⚠ El empleado no tiene correo electrónico registrado")
		return False, None
	
	if not empleado.usuario:
		print("⚠ El empleado no tiene usuario")
		return False, None
	
	from django.conf import settings
	import string
	import random
	
	# Generar contraseña temporal aleatoria (12 caracteres)
	caracteres = string.ascii_letters + string.digits + '!@#$%^&*'
	password_temporal = ''.join(random.choice(caracteres) for _ in range(12))
	
	# URL del sistema
	url_sistema = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
	url_login = f"{url_sistema}/login/"
	
	# Preparar contexto para la plantilla
	context = {
		'nombre': empleado.nombre_completo,
		'usuario': empleado.usuario,
		'password': password_temporal,
		'email': empleado.email,
		'url_login': url_login,
		'razon_social': config.razon_social,
		'nombre_corto': config.nombre_corto,
	}
	
	# Renderizar HTML del correo
	html_message = render_to_string('desarrollo/web/email_bienvenida_credenciales.html', context)
	
	# Crear mensaje de texto
	text_content = f"""
Hola {empleado.nombre_completo},

Te enviamos tu nueva contraseña de acceso al Sistema de Vivienda {config.razon_social}.

TUS CREDENCIALES DE ACCESO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usuario: {empleado.usuario}
Contraseña: {password_temporal}
Email: {empleado.email}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️ IMPORTANTE - TEN CUIDADO CON TUS CREDENCIALES:
• Guarda esta información en un lugar seguro
• NO compartas tu contraseña con nadie
• Cambia tu contraseña periódicamente después de iniciar sesión
• NO uses la misma contraseña en otros sistemas

Puedes acceder al sistema en:
{url_login}

Saludos cordiales,
Equipo {config.razon_social}
	""".strip()
	
	try:
		# Actualizar la contraseña del empleado
		empleado.set_password(password_temporal)
		empleado.save()
		
		# Usar la función de utilidad para envío con fallback
		guardar_correo_en_cola(
			tipo_correo='credenciales',
			email_destino=empleado.email,
			asunto=f"Tus credenciales de acceso actualizadas - {config.nombre_corto}",
			contenido_texto=text_content,
			contenido_html=html_message,
			id_empleado=empleado.id_empleado
		)
		cola = ColaCorreos.objects.filter(email_destino=empleado.email).last()
		if cola:
			cola.estado = 'enviado'
			cola.fecha_envio = timezone.now()
			cola.save()
		
		print(f"✓ Credenciales actualizadas y guardadas en cola para {empleado.email}")
		return True, password_temporal
		
	except Exception as e:
		error_msg = str(e)
		print(f"✗ Error al guardar credenciales: {error_msg}")
		return False, None

