"""
Middleware para manejar el timeout de sesión dinámico basado en ConfiguracionSistema
"""
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.timezone import now
from datetime import timedelta


class SessionTimeoutMiddleware:
	"""
	Middleware que controla el timeout de sesión dinámicamente
	basado en el valor configurado en ConfiguracionSistema.tiempo_sesion_minutos
	"""
	
	def __init__(self, get_response):
		self.get_response = get_response
	
	def __call__(self, request):
		# Si el usuario está autenticado
		if request.user.is_authenticated:
			# Obtener el tiempo de sesión configurado
			try:
				from portal.models import ConfiguracionSistema
				config = ConfiguracionSistema.objects.first()
				tiempo_sesion_minutos = config.tiempo_sesion_minutos if config else 15
			except:
				tiempo_sesion_minutos = 15
			
			# Convertir a segundos
			tiempo_sesion_segundos = tiempo_sesion_minutos * 60
			
			# Obtener el timestamp de la última actividad de la sesión
			ultima_actividad = request.session.get('ultima_actividad')
			
			if ultima_actividad:
				# Calcular tiempo transcurrido desde la última actividad
				ultima_actividad_time = float(ultima_actividad)
				tiempo_actual = now().timestamp()
				tiempo_transcurrido = tiempo_actual - ultima_actividad_time
				
				# Si ha pasado el tiempo configurado, cerrar sesión
				if tiempo_transcurrido > tiempo_sesion_segundos:
					logout(request)
					messages.warning(request, 'Tu sesión expiró por inactividad. Ingresa nuevamente para continuar.')
					return redirect('index')
			
			# Actualizar el timestamp de última actividad
			request.session['ultima_actividad'] = now().timestamp()
		
		response = self.get_response(request)
		return response
