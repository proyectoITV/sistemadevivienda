from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError


def _current_year():
	return timezone.now().year


class Anuncio(models.Model):
	titulo = models.CharField(max_length=200)
	contenido = models.TextField()
	fecha_publicacion = models.DateTimeField(auto_now_add=True)
	activo = models.BooleanField(default=True)

	def __str__(self):
		return self.titulo


class SeguridadContactanos(models.Model):
	uuid_folio = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
	nombre_completo = models.CharField(max_length=180)
	email = models.EmailField(max_length=254)
	compania_organizacion = models.CharField(max_length=180, blank=True)
	telefono = models.CharField(max_length=30, blank=True)
	asunto = models.CharField(max_length=200)
	mensaje = models.TextField()
	fecha_hora_insercion = models.DateTimeField(auto_now_add=True)
	ip_origen = models.GenericIPAddressField(null=True, blank=True)
	user_agent = models.TextField(blank=True)
	leido = models.BooleanField(default=False)
	fecha_lectura = models.DateTimeField(null=True, blank=True)

	class Meta:
		db_table = 'seguridad_contactanos'
		verbose_name = 'Contacto'
		verbose_name_plural = 'Contactos'
		ordering = ['-fecha_hora_insercion']

	def __str__(self):
		return f"{self.nombre_completo} - {self.asunto}"

class CatalogosEntidadesFederativas(models.Model):
	nombre = models.CharField(max_length=100, unique=True)
	clave = models.CharField(max_length=2, unique=True)
	
	class Meta:
		db_table = 'catalogos_entidadesfederativas'
		verbose_name = 'Entidad Federativa'
		verbose_name_plural = 'Entidades Federativas'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class CatalogosMunicipios(models.Model):
	entidad = models.ForeignKey(CatalogosEntidadesFederativas, on_delete=models.CASCADE, related_name='municipios')
	nombre = models.CharField(max_length=100)
	clave = models.CharField(max_length=3, blank=True)
	
	class Meta:
		db_table = 'catalogos_municipios'
		verbose_name = 'Municipio'
		verbose_name_plural = 'Municipios'
		ordering = ['entidad', 'nombre']
		unique_together = ('entidad', 'nombre')
	
	def __str__(self):
		return f"{self.nombre} ({self.entidad})"


class SeguridadConfiguracionDelSistema(models.Model):
	razon_social = models.CharField(max_length=255)
	nombre_corto = models.CharField(max_length=100)
	rfc = models.CharField(max_length=13, unique=True)
	domicilio = models.CharField(max_length=255)
	numero_exterior = models.CharField(max_length=20)
	colonia = models.CharField(max_length=150)
	codigo_postal = models.CharField(max_length=5)
	id_municipio = models.ForeignKey(CatalogosMunicipios, on_delete=models.SET_NULL, null=True)
	
	# Configuración SMTP
	smtp_host = models.CharField(max_length=255, blank=True, help_text='Ej: smtp.gmail.com')
	smtp_puerto = models.IntegerField(default=587, help_text='Puerto SMTP (587 para TLS, 465 para SSL)')
	smtp_usuario = models.CharField(max_length=255, blank=True)
	smtp_contrasena = models.CharField(max_length=255, blank=True)
	smtp_usar_tls = models.BooleanField(default=True)
	smtp_usar_ssl = models.BooleanField(default=False)
	correo_remitente = models.EmailField(blank=True, help_text='Correo desde el que se enviarán notificaciones')
	
	# Configuración adicional
	activo = models.BooleanField(default=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'seguridad_configuraciondelsistema'
		verbose_name = 'Configuración del Sistema'
		verbose_name_plural = 'Configuración del Sistema'
	
	def __str__(self):
		return self.razon_social


class CatalogosDelegaciones(models.Model):
	municipio = models.ForeignKey(CatalogosMunicipios, on_delete=models.CASCADE, related_name='delegaciones', null=True, blank=True)
	nombre = models.CharField(max_length=150, unique=True)
	telefono = models.CharField(max_length=30)
	correo = models.EmailField(blank=True)
	direccion = models.CharField(max_length=255, help_text='Dirección completa para georreferenciación')
	latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	horario = models.CharField(max_length=100, blank=True, help_text='Ej: Lun-Vie 8:00-17:00')
	responsable = models.CharField(max_length=150, blank=True)
	foto = models.ImageField(upload_to='delegaciones/', blank=True, null=True)
	activo = models.BooleanField(default=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		db_table = 'catalogos_delegaciones'
		verbose_name = 'Delegación'
		verbose_name_plural = 'Delegaciones'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class PersonalDireccion(models.Model):
	iddireccion = models.AutoField(primary_key=True)
	direccion = models.CharField(max_length=200, unique=True, help_text='Nombre de la dirección')
	descripcion = models.TextField(blank=True, help_text='Descripción adicional de la dirección')
	ordenjerarquia = models.IntegerField(default=0, help_text='Orden jerárquico para la dirección')
	activo = models.BooleanField(default=True, help_text='Indica si la dirección está vigente')
	fecha_captura = models.DateTimeField(auto_now_add=True, help_text='Fecha cuando se registró la dirección')
	fecha_modificacion = models.DateTimeField(auto_now=True, help_text='Fecha de la última modificación')
	usuario_captura = models.CharField(max_length=100, blank=True, help_text='Usuario que capturó el registro')
	usuario_modificacion = models.CharField(max_length=100, blank=True, help_text='Usuario que modificó el registro')
	
	class Meta:
		db_table = 'personal_direccion'
		verbose_name = 'Dirección'
		verbose_name_plural = 'Direcciones'
		ordering = ['ordenjerarquia', 'direccion']
	
	def __str__(self):
		return self.direccion


class PersonalDepartamento(models.Model):
	iddepartamento = models.AutoField(primary_key=True)
	departamento = models.CharField(max_length=200, unique=True, help_text='Nombre del departamento')
	iddireccion = models.ForeignKey(PersonalDireccion, on_delete=models.CASCADE, related_name='departamentos', help_text='Dirección a la que pertenece')
	descripcion = models.TextField(blank=True, help_text='Descripción adicional del departamento')
	ordenjerarquia = models.IntegerField(default=0, help_text='Orden jerárquico para el departamento')
	activo = models.BooleanField(default=True, help_text='Indica si el departamento está vigente')
	fecha_captura = models.DateTimeField(auto_now_add=True, help_text='Fecha cuando se registró el departamento')
	fecha_modificacion = models.DateTimeField(auto_now=True, help_text='Fecha de la última modificación')
	usuario_captura = models.CharField(max_length=100, blank=True, help_text='Usuario que capturó el registro')
	usuario_modificacion = models.CharField(max_length=100, blank=True, help_text='Usuario que modificó el registro')
	
	class Meta:
		db_table = 'personal_departamento'
		verbose_name = 'Departamento'
		verbose_name_plural = 'Departamentos'
		ordering = ['iddireccion__ordenjerarquia', 'ordenjerarquia', 'departamento']
	
	def __str__(self):
		return self.departamento


class PersonalTipoDeContratacion(models.Model):
	idtipodecontratacion = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=100, unique=True, help_text='Nombre del tipo de contratación')
	descripcion = models.TextField(blank=True, help_text='Descripción del tipo de contratación')
	activo = models.BooleanField(default=True, help_text='Indica si el tipo de contratación está vigente')
	fecha_captura = models.DateTimeField(auto_now_add=True, help_text='Fecha cuando se registró el tipo')
	fecha_modificacion = models.DateTimeField(auto_now=True, help_text='Fecha de la última modificación')
	usuario_captura = models.CharField(max_length=100, blank=True, help_text='Usuario que capturó el registro')
	usuario_modificacion = models.CharField(max_length=100, blank=True, help_text='Usuario que modificó el registro')
	
	class Meta:
		db_table = 'personal_tipodecontratacion'
		verbose_name = 'Tipo de Contratación'
		verbose_name_plural = 'Tipos de Contratación'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class PersonalPuestos(models.Model):
	idpuesto = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=150, unique=True, help_text='Nombre del puesto')
	descripcion = models.TextField(blank=True, help_text='Descripción del puesto')
	activo = models.BooleanField(default=True, help_text='Indica si el puesto está vigente')
	fecha_captura = models.DateTimeField(auto_now_add=True, help_text='Fecha cuando se registró el puesto')
	fecha_modificacion = models.DateTimeField(auto_now=True, help_text='Fecha de la última modificación')
	usuario_captura = models.CharField(max_length=100, blank=True, help_text='Usuario que capturó el registro')
	usuario_modificacion = models.CharField(max_length=100, blank=True, help_text='Usuario que modificó el registro')
	
	class Meta:
		db_table = 'personal_puestos'
		verbose_name = 'Puesto'
		verbose_name_plural = 'Puestos'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class UsuarioManager(BaseUserManager):
	def create_user(self, usuario, email, password=None, **extra_fields):
		# usuario puede ser None si se crea un empleado sin credenciales de autenticación
		if not email:
			raise ValueError('El empleado debe tener un correo electrónico')
		
		user = self.model(
			usuario=usuario,
			email=self.normalize_email(email),
			**extra_fields
		)
		if password:
			user.set_password(password)
		else:
			user.set_unusable_password()
		user.save(using=self._db)
		return user
	
	def create_superuser(self, usuario, email, password=None, **extra_fields):
		extra_fields.setdefault('is_admin', True)
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('El superusuario debe tener is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('El superusuario debe tener is_superuser=True.')

		return self.create_user(usuario, email, password, **extra_fields)


class PersonalEmpleados(AbstractBaseUser, PermissionsMixin):
	"""Modelo de Empleados con campos de Recursos Humanos y autenticación"""
	
	# Identificación
	id_empleado = models.AutoField(primary_key=True)
	usuario = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text='Nombre de usuario para login')
	email = models.EmailField(unique=True)
	
	# Nombre dividido
	apellido_paterno = models.CharField(max_length=100, help_text='Apellido paterno del empleado')
	apellido_materno = models.CharField(max_length=100, blank=True, help_text='Apellido materno del empleado')
	nombre = models.CharField(max_length=100, help_text='Nombre(s) del empleado')
	nombre_completo = models.CharField(max_length=200, editable=False, help_text='Se genera automáticamente')
	
	# Información personal
	curp = models.CharField(max_length=18, unique=True, blank=True)
	rfc = models.CharField(max_length=13, unique=True, blank=True)
	fecha_nacimiento = models.DateField(null=True, blank=True)
	sexo = models.CharField(max_length=1, choices=[('M', 'Masculino'), ('F', 'Femenino')], blank=True)
	telefono = models.CharField(max_length=20, blank=True)
	domicilio = models.TextField(blank=True)
	fotografia = models.ImageField(upload_to='empleados/fotos/', null=True, blank=True, help_text='Fotografía del empleado')
	
	# Información laboral
	iddepartamento = models.ForeignKey(PersonalDepartamento, on_delete=models.SET_NULL, null=True, blank=True, help_text='Departamento del empleado')
	idpuesto = models.ForeignKey(PersonalPuestos, on_delete=models.SET_NULL, null=True, blank=True, help_text='Puesto del empleado')
	numero_empleado = models.CharField(max_length=20, unique=True, blank=True)
	fecha_ingreso = models.DateField(null=True, blank=True)
	idtipodecontratacion = models.ForeignKey(PersonalTipoDeContratacion, on_delete=models.SET_NULL, null=True, blank=True, help_text='Tipo de contratación del empleado')
	salario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
	activo = models.BooleanField(default=True)
	
	# Seguridad y control
	recordar_dispositivo = models.BooleanField(default=False, help_text='Permite recordar este dispositivo')
	token_dispositivo = models.CharField(max_length=255, blank=True, unique=True, null=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	
	# Auditoría
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	fecha_ultimo_login = models.DateTimeField(null=True, blank=True)
	
	groups = models.ManyToManyField('auth.Group', blank=True, related_name='personal_empleados_groups')
	user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='personal_empleados_permissions')
	
	objects = UsuarioManager()
	
	USERNAME_FIELD = 'usuario'
	REQUIRED_FIELDS = ['email', 'apellido_paterno', 'nombre']
	
	def save(self, *args, **kwargs):
		"""Generar nombre_completo automáticamente"""
		if self.apellido_materno:
			self.nombre_completo = f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
		else:
			self.nombre_completo = f"{self.nombre} {self.apellido_paterno}"
		super().save(*args, **kwargs)
	
	class Meta:
		db_table = 'personal_empleados'
		verbose_name = 'Empleado'
		verbose_name_plural = 'Empleados'
		ordering = ['nombre_completo']
	
	def __str__(self):
		if self.usuario:
			return f"{self.nombre_completo} ({self.usuario})"
		return self.nombre_completo


class RecuperacionContrasena(models.Model):
	usuario = models.ForeignKey(PersonalEmpleados, on_delete=models.CASCADE, related_name='recuperaciones')
	token = models.CharField(max_length=255, unique=True, db_index=True)
	email = models.EmailField()
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_expiracion = models.DateTimeField()
	utilizado = models.BooleanField(default=False)
	fecha_uso = models.DateTimeField(null=True, blank=True)
	ip_origen = models.GenericIPAddressField(null=True, blank=True)
	
	class Meta:
		db_table = 'recuperacion_contrasena'
		verbose_name = 'Recuperación de Contraseña'
		verbose_name_plural = 'Recuperaciones de Contraseña'
		ordering = ['-fecha_creacion']
	
	def esta_vigente(self):
		return not self.utilizado and timezone.now() < self.fecha_expiracion
	
	def __str__(self):
		return f"Recuperación para {self.usuario.usuario} - {self.fecha_creacion}"
	
	@classmethod
	def crear_token_recuperacion(cls, usuario, ip_origen=None):
		"""Crea un nuevo token de recuperación válido por 24 horas"""
		from django.utils.crypto import get_random_string
		
		token = get_random_string(50)
		fecha_expiracion = timezone.now() + timedelta(hours=24)
		
		recuperacion = cls.objects.create(
			usuario=usuario,
			token=token,
			email=usuario.email,
			fecha_expiracion=fecha_expiracion,
			ip_origen=ip_origen
		)
		return recuperacion


class ConfiguracionSistema(models.Model):
	"""Configuración general del sistema ITAVU"""
	
	razon_social = models.CharField(max_length=255, help_text='Razón social de la empresa')
	nombre_corto = models.CharField(max_length=50, help_text='Nombre corto de la empresa (ej: ITAVU)')
	rfc = models.CharField(max_length=13, unique=True, help_text='RFC de la empresa')
	domicilio = models.TextField(help_text='Domicilio de la empresa')
	
	# SMTP Configuration
	smtp_host = models.CharField(max_length=255, blank=True, help_text='Servidor SMTP (ej: smtp.gmail.com)')
	smtp_port = models.IntegerField(default=587, help_text='Puerto SMTP (ej: 587)')
	smtp_usuario = models.CharField(max_length=255, blank=True, help_text='Usuario SMTP')
	smtp_contrasena = models.CharField(max_length=255, blank=True, help_text='Contraseña SMTP')
	smtp_usar_tls = models.BooleanField(default=True, help_text='Usar TLS en SMTP')
	email_desde = models.EmailField(help_text='Email desde el cual se enviarán los correos')
	
	# Información adicional
	telefono = models.CharField(max_length=20, blank=True)
	sitio_web = models.URLField(blank=True)
	logo = models.ImageField(upload_to='sistema/', null=True, blank=True)
	
	# Configuración de sesiones y seguridad
	tiempo_sesion_minutos = models.IntegerField(
		default=15,
		help_text='Tiempo de inactividad en minutos para cerrar la sesión (default: 15 minutos)'
	)
	
	# Configuración de intro
	duracion_intro_segundos = models.IntegerField(
		default=3,
		help_text='Duración de la pantalla de introducción en segundos (1-6)',
		validators=[MinValueValidator(1), MaxValueValidator(6)]
	)
	departamento_soporte_mantenimiento = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='configuraciones_soporte_mantenimiento',
		help_text='Departamento que atenderá los tickets de Servicio de Mantenimiento'
	)
	departamento_compras_requisiciones = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='configuraciones_compras_requisiciones',
		help_text='Departamento que atenderá Requisiciones y el módulo de Compras'
	)
	
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'configuracion_sistema'
		verbose_name = 'Configuración del Sistema'
		verbose_name_plural = 'Configuración del Sistema'
	
	def __str__(self):
		return f"Configuración: {self.nombre_corto}"


class UsuariosDelSistema(models.Model):
	"""Usuarios del sistema de ITAVU"""
	
	ROLES_CHOICES = [
		('admin', 'Administrador'),
		('supervisor', 'Supervisor'),
		('empleado', 'Empleado'),
		('viewer', 'Visualizador'),
	]
	
	id_usuario_sistema = models.AutoField(primary_key=True)
	id_empleado = models.OneToOneField(PersonalEmpleados, on_delete=models.CASCADE, related_name='usuario_sistema', help_text='Empleado asociado')
	
	usuario = models.CharField(max_length=100, unique=True, help_text='Nombre de usuario para login')
	correo = models.EmailField(unique=True, help_text='Correo electrónico')
	contrasena = models.CharField(max_length=255, help_text='Contraseña encriptada')
	
	rol = models.CharField(max_length=20, choices=ROLES_CHOICES, default='empleado', help_text='Rol del usuario')
	
	activo = models.BooleanField(default=True, help_text='¿El usuario está activo?')
	requiere_cambio_contrasena = models.BooleanField(default=True, help_text='¿Requiere cambiar contraseña?')
	
	fecha_ultimo_login = models.DateTimeField(null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	creado_por = models.ForeignKey(PersonalEmpleados, on_delete=models.SET_NULL, null=True, related_name='usuarios_creados', help_text='Usuario que creó este registro')
	
	class Meta:
		db_table = 'usuarios_del_sistema'
		verbose_name = 'Usuario del Sistema'
		verbose_name_plural = 'Usuarios del Sistema'
		ordering = ['-fecha_creacion']
	
	def __str__(self):
		return f"{self.usuario} ({self.id_empleado.nombre_completo})"


class ColaCorreos(models.Model):
	"""Cola de correos para gestionar envíos con límite de 2000 diarios"""
	
	TIPO_CORREO_CHOICES = [
		('bienvenida', 'Bienvenida con Credenciales'),
		('recuperacion', 'Recuperación de Contraseña'),
		('credenciales', 'Reenvío de Credenciales'),
		('contacto', 'Confirmación de Contacto'),
		('otro', 'Otro'),
	]
	
	ESTADO_CHOICES = [
		('pendiente', 'Pendiente'),
		('enviado', 'Enviado Correctamente'),
		('error', 'Error'),
	]
	
	id_cola = models.AutoField(primary_key=True)
	tipo_correo = models.CharField(max_length=20, choices=TIPO_CORREO_CHOICES, help_text='Tipo de correo')
	email_destino = models.EmailField(help_text='Correo destino')
	asunto = models.CharField(max_length=255, help_text='Asunto del correo')
	contenido_texto = models.TextField(help_text='Contenido en texto plano')
	contenido_html = models.TextField(help_text='Contenido en HTML')
	
	# Estado del envío
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
	mensaje_error = models.TextField(blank=True, help_text='Mensaje de error si falló el envío')
	
	# Auditoría
	fecha_creacion = models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del registro')
	fecha_envio = models.DateTimeField(null=True, blank=True, help_text='Fecha cuando se envió correctamente')
	numero_intentos = models.IntegerField(default=0, help_text='Número de intentos de envío')
	
	# Relación con empleado (opcional)
	id_empleado = models.ForeignKey(PersonalEmpleados, on_delete=models.SET_NULL, null=True, blank=True, related_name='correos_cola')
	
	class Meta:
		db_table = 'cola_correos'
		verbose_name = 'Cola de Correos'
		verbose_name_plural = 'Cola de Correos'
		ordering = ['-fecha_creacion']
		indexes = [
			models.Index(fields=['estado', 'fecha_creacion']),
			models.Index(fields=['email_destino']),
		]
	
	def __str__(self):
		return f"{self.get_tipo_correo_display()} - {self.email_destino} ({self.get_estado_display()})"

# ==================== MODELOS DE TRANSPARENCIA ====================
class TransparenciaGo(models.Model):
	"""Archivos publicados en el modulo de transparencia."""
	id_file = models.AutoField(primary_key=True, db_column='IdFile')
	file_nombre = models.CharField(max_length=255, db_column='FileNombre', help_text='Nombre del archivo original')
	id_user = models.CharField(max_length=255, db_column='IdUser', help_text='Usuario que subio el archivo')
	fecha = models.DateField(db_column='fecha')
	hora = models.TimeField(db_column='hora')
	file_descripcion = models.TextField(db_column='FileDescripcion', blank=True, help_text='Descripcion del archivo')

	class Meta:
		db_table = 'TransparenciaGo'
		verbose_name = 'Archivo de Transparencia'
		verbose_name_plural = 'Archivos de Transparencia'
		ordering = ['fecha', 'hora', 'id_file']

	def __str__(self):
		return f"{self.file_nombre} ({self.fecha} {self.hora})"


# ==================== MODELOS DE PATRIMONIO ====================

class CatalogosMarcas(models.Model):
	"""Catálogo de marcas de artículos"""
	idmarca = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=150, unique=True, help_text='Nombre de la marca')
	descripcion = models.TextField(blank=True, help_text='Descripción adicional')
	activo = models.BooleanField(default=True, help_text='¿La marca está activa?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'catalogos_marcas'
		verbose_name = 'Marca'
		verbose_name_plural = 'Marcas'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class PatrimonioClasificacionSerap(models.Model):
	"""Clasificación SERAP de artículos"""
	idclasificacion_serap = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=150, unique=True, help_text='Nombre de la clasificación SERAP')
	descripcion = models.TextField(blank=True, help_text='Descripción adicional')
	activo = models.BooleanField(default=True, help_text='¿La clasificación está activa?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'patrimonio_clasificacionserap'
		verbose_name = 'Clasificación SERAP'
		verbose_name_plural = 'Clasificaciones SERAP'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class PatrimonioClasificacionContraloria(models.Model):
	"""Clasificación de Contraloría de artículos"""
	idclasificacion_contraloria = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=150, unique=True, help_text='Nombre de la clasificación de Contraloría')
	descripcion = models.TextField(blank=True, help_text='Descripción adicional')
	activo = models.BooleanField(default=True, help_text='¿La clasificación está activa?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'patrimonio_clasificacioncontraloria'
		verbose_name = 'Clasificación de Contraloría'
		verbose_name_plural = 'Clasificaciones de Contraloría'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class PatrimonioEstatusArticulo(models.Model):
	"""Estatus de los artículos del patrimonio"""
	STATUS_CHOICES = [
		(0, 'Activo'),
		(1, 'Eliminado'),
	]
	
	idestatusarticulo = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=200, unique=True, help_text='Descripción del estatus')
	idestatus = models.IntegerField(choices=STATUS_CHOICES, default=0, help_text='Estado del estatus (0=activo, 1=eliminado)')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'patrimonio_estatusdelarticulo'
		verbose_name = 'Estatus del Artículo'
		verbose_name_plural = 'Estatus de Artículos'
		ordering = ['descripcion']
	
	def __str__(self):
		return self.descripcion


class PatrimonioEstatusDelRegistro(models.Model):
	"""Estatus del registro de artículos en el patrimonio"""
	idestatus = models.AutoField(primary_key=True)
	descripcion = models.CharField(max_length=200, unique=True, help_text='Descripción del estatus del registro')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'patrimonio_estatusdelregistro'
		verbose_name = 'Estatus del Registro'
		verbose_name_plural = 'Estatus de Registros'
		ordering = ['idestatus']
	
	def __str__(self):
		return self.descripcion


class PatrimonioProveedor(models.Model):
	"""Proveedores de artículos"""
	idproveedor = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200, unique=True, help_text='Nombre del proveedor')
	rfc = models.CharField(max_length=13, blank=True, null=True, unique=True, help_text='RFC del proveedor')
	telefono = models.CharField(max_length=20, blank=True, null=True, help_text='Teléfono del proveedor')
	correo = models.EmailField(blank=True, null=True, help_text='Correo del proveedor')
	domicilio = models.TextField(blank=True, null=True, help_text='Domicilio del proveedor')
	persona_contacto = models.CharField(max_length=200, blank=True, null=True, help_text='Persona de contacto')
	descripcion = models.TextField(blank=True, null=True, help_text='Descripción adicional')
	activo = models.BooleanField(default=True, help_text='¿El proveedor está activo?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'patrimonio_proveedor'
		verbose_name = 'Proveedor'
		verbose_name_plural = 'Proveedores'
		ordering = ['nombre']
	
	def __str__(self):
		return self.nombre


class PatrimonioBienesDelInstituto(models.Model):
	"""Registro de bienes del Instituto"""
	idbien = models.AutoField(primary_key=True)
	numero_inventario_itavu = models.CharField(max_length=50, unique=True, help_text='Número de inventario ITAVU')
	numero_inventario_gobierno = models.CharField(max_length=50, blank=True, help_text='Número de inventario Gobierno')
	descripcion = models.CharField(max_length=255, help_text='Descripción del bien')
	fotografia = models.ImageField(upload_to='patrimonio/fotos/', null=True, blank=True, help_text='Fotografía del bien')
	fecha_registro = models.DateField(auto_now_add=True, help_text='Fecha de registro')
	
	# Especificaciones técnicas
	marca = models.ForeignKey(CatalogosMarcas, on_delete=models.SET_NULL, null=True, blank=True, help_text='Marca del bien')
	modelo = models.CharField(max_length=100, blank=True, help_text='Modelo del bien')
	serie = models.CharField(max_length=100, blank=True, unique=True, help_text='Número de serie')
	# Tipo de equipo (computadora/otro)
	tipo_equipo = models.CharField(
		max_length=20,
		choices=[('computadora', 'Computadora/PC'), ('otro', 'Otro')],
		default='otro',
		help_text='Tipo de equipo (para campos de monitor)',
	)
	numinv_monitor = models.CharField(max_length=50, blank=True, help_text='Número de inventario del monitor emparejado')
	numserie_monitor = models.CharField(max_length=50, blank=True, help_text='Número de serie del monitor emparejado')
	
	# Información de compra
	fecha_factura = models.DateField(null=True, blank=True, help_text='Fecha de facturación')
	numero_factura = models.CharField(max_length=50, blank=True, unique=True, help_text='Número de factura')
	costo_articulo = models.DecimalField(max_digits=12, decimal_places=2, help_text='Costo del artículo')
	proveedor = models.ForeignKey(PatrimonioProveedor, on_delete=models.SET_NULL, null=True, blank=True, help_text='Proveedor del bien')
	archivo_factura = models.FileField(upload_to='patrimonio/facturas/', null=True, blank=True, help_text='Archivo PDF de la factura')
	
	# Clasificaciones
	clasificacion_serap = models.ForeignKey(PatrimonioClasificacionSerap, on_delete=models.SET_NULL, null=True, blank=True, help_text='Clasificación SERAP')
	clasificacion_contraloria = models.ForeignKey(PatrimonioClasificacionContraloria, on_delete=models.SET_NULL, null=True, blank=True, help_text='Clasificación de Contraloría')
	
	# Estatus del registro y baja
	idestatus = models.ForeignKey(PatrimonioEstatusDelRegistro, on_delete=models.SET_NULL, null=True, blank=True, default=1, help_text='Estatus del registro en el patrimonio')
	baja_fecha = models.DateField(null=True, blank=True, help_text='Fecha de baja del bien')
	baja_numero_oficio = models.CharField(max_length=100, blank=True, help_text='Número del oficio de baja')
	baja_oficio = models.FileField(upload_to='patrimonio/bajas/', null=True, blank=True, help_text='Archivo PDF del oficio de baja')
	
	# Información adicional
	observaciones = models.TextField(blank=True, help_text='Observaciones sobre el bien')
	
	# Auditoría
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	usuario_captura = models.CharField(max_length=100, blank=True, help_text='Usuario que capturó el registro')
	usuario_modificacion = models.CharField(max_length=100, blank=True, help_text='Usuario que modificó el registro')
	
	class Meta:
		db_table = 'patrimonio_bienes'
		verbose_name = 'Bien del Instituto'
		verbose_name_plural = 'Bienes del Instituto'
		ordering = ['-fecha_creacion']
		indexes = [
			models.Index(fields=['numero_inventario_itavu']),
			models.Index(fields=['numero_inventario_gobierno']),
			models.Index(fields=['idestatus']),
		]
	
	def __str__(self):
		return f"{self.numero_inventario_itavu} - {self.descripcion}"


class PatrimonioResguardo(models.Model):
	"""Resguardos internos de bienes - Historial de asignaciones a empleados"""
	idresguardo = models.AutoField(primary_key=True)
	bien = models.ForeignKey(PatrimonioBienesDelInstituto, on_delete=models.CASCADE, related_name='resguardos', help_text='Bien resguardado')
	empleado = models.ForeignKey(PersonalEmpleados, on_delete=models.PROTECT, related_name='resguardos', help_text='Empleado responsable')
	
	# Fechas de asignación y devolución
	fecha_asignacion = models.DateField(help_text='Fecha de asignación del bien')
	fecha_devolucion = models.DateField(null=True, blank=True, help_text='Fecha de devolución del bien')
	
	# Información del oficio
	numero_oficio = models.CharField(max_length=100, blank=True, help_text='Número de oficio de asignación')
	fecha_oficio = models.DateField(null=True, blank=True, help_text='Fecha del oficio de asignación')
	archivo_oficio = models.FileField(upload_to='patrimonio/oficios/', null=True, blank=True, help_text='PDF del oficio de asignación')
	
	# Observaciones
	observaciones_asignacion = models.TextField(blank=True, help_text='Observaciones al momento de asignar')
	observaciones_devolucion = models.TextField(blank=True, help_text='Observaciones al momento de devolver')
	
	# Estado del resguardo
	activo = models.BooleanField(default=True, help_text='¿Es el resguardo actual?')
	
	# Auditoría
	usuario_asignacion = models.CharField(max_length=100, blank=True, help_text='Usuario que realizó la asignación')
	usuario_devolucion = models.CharField(max_length=100, blank=True, help_text='Usuario que registró la devolución')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'patrimonio_resguardos'
		verbose_name = 'Resguardo de Bien'
		verbose_name_plural = 'Resguardos de Bienes'
		ordering = ['-fecha_asignacion']
		indexes = [
			models.Index(fields=['bien', 'activo']),
			models.Index(fields=['empleado', 'activo']),
			models.Index(fields=['fecha_asignacion']),
		]
	
	def __str__(self):
		estado = "ACTIVO" if self.activo else "DEVUELTO"
		return f"{self.bien.numero_inventario_itavu} → {self.empleado.nombre} {self.empleado.apellido_paterno} [{estado}]"


class PatrimonioEntregaDepartamento(models.Model):
	"""Acta operativa de entrega-recepción de bienes entre empleados del mismo departamento"""
	identrega = models.AutoField(primary_key=True)
	empleado_saliente = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.PROTECT,
		related_name='entregas_departamento_saliente',
		help_text='Empleado que entrega los bienes'
	)
	empleado_entrante = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.PROTECT,
		related_name='entregas_departamento_entrante',
		help_text='Empleado que recibe los bienes'
	)
	departamento = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.PROTECT,
		related_name='entregas_departamento',
		help_text='Departamento al que corresponde la entrega'
	)
	fecha_entrega = models.DateField(help_text='Fecha de entrega-recepción')
	observaciones = models.TextField(blank=True, help_text='Observaciones generales de la entrega')
	total_bienes = models.PositiveIntegerField(default=0, help_text='Cantidad de bienes transferidos')

	# Auditoría
	usuario_registro = models.CharField(max_length=100, blank=True, help_text='Usuario que registró la entrega')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'patrimonio_entrega_departamento'
		verbose_name = 'Entrega de Departamento'
		verbose_name_plural = 'Entregas de Departamento'
		ordering = ['-fecha_entrega', '-fecha_creacion']
		indexes = [
			models.Index(fields=['departamento', 'fecha_entrega']),
			models.Index(fields=['empleado_saliente']),
			models.Index(fields=['empleado_entrante']),
		]

	def __str__(self):
		return f"Entrega #{self.identrega} - {self.departamento.departamento} ({self.fecha_entrega})"


class PatrimonioEntregaDepartamentoDetalle(models.Model):
	"""Detalle de bienes transferidos en una entrega-recepción de departamento"""
	iddetalle = models.AutoField(primary_key=True)
	entrega = models.ForeignKey(
		PatrimonioEntregaDepartamento,
		on_delete=models.CASCADE,
		related_name='detalles',
		help_text='Entrega de departamento'
	)
	bien = models.ForeignKey(
		PatrimonioBienesDelInstituto,
		on_delete=models.PROTECT,
		related_name='entregas_departamento',
		help_text='Bien transferido'
	)
	resguardo_anterior = models.ForeignKey(
		PatrimonioResguardo,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='detalles_entrega_anterior',
		help_text='Resguardo que se cierra'
	)
	resguardo_nuevo = models.ForeignKey(
		PatrimonioResguardo,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='detalles_entrega_nuevo',
		help_text='Resguardo creado para el empleado entrante'
	)
	fecha_transferencia = models.DateField(help_text='Fecha de transferencia del bien')
	observaciones = models.TextField(blank=True, help_text='Observaciones del bien transferido')

	class Meta:
		db_table = 'patrimonio_entrega_departamento_detalle'
		verbose_name = 'Detalle de Entrega de Departamento'
		verbose_name_plural = 'Detalles de Entrega de Departamento'
		ordering = ['iddetalle']
		constraints = [
			models.UniqueConstraint(fields=['entrega', 'bien'], name='unique_bien_por_entrega_departamento')
		]

	def __str__(self):
		return f"Entrega #{self.entrega.identrega} - {self.bien.numero_inventario_itavu}"


# ==================== MODELOS DE FONDO ECONÓMICO DE RESERVA (FER) ====================

class CatalogosSexo(models.Model):
	"""Catálogo de sexos para información personal"""
	idsexo = models.AutoField(primary_key=True)
	sexo = models.CharField(max_length=50, unique=True, help_text='Descripción del sexo')
	activo = models.BooleanField(default=True, help_text='¿El catálogo está activo?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'catalogos_sexo'
		verbose_name = 'Sexo'
		verbose_name_plural = 'Sexos'
		ordering = ['idsexo']
	
	def __str__(self):
		return self.sexo


class CatalogosAdministraciones(models.Model):
	"""Administraciones (periodos de gobierno) usados para filtrar registros FER"""
	idadministracion = models.AutoField(primary_key=True)
	fechainicio = models.DateField(help_text='Fecha de inicio de la administración')
	fechatermino = models.DateField(help_text='Fecha de término de la administración')
	fecha_creacion = models.DateTimeField(help_text='Fecha de creación del registro')
	id_empleado = models.IntegerField(help_text='ID del empleado responsable')
	gobernador = models.CharField(max_length=255, help_text='Nombre del gobernador')

	class Meta:
		db_table = 'catalogos_administraciones'
		verbose_name = 'Administración'
		verbose_name_plural = 'Administraciones'
		ordering = ['-fechainicio']

	def __str__(self):
		return f"{self.gobernador} ({self.fechainicio.year}-{self.fechatermino.year})"


class FerFondos(models.Model):
	"""Fondos disponibles por ejercicio fiscal para el Fondo Económico de Reserva"""
	idfondo = models.AutoField(primary_key=True)
	fondo = models.BigIntegerField(help_text='Cantidad del fondo disponible')
	ejercicio = models.IntegerField(unique=True, help_text='Año fiscal')
	fechainicio = models.DateField(help_text='Fecha de inicio del fondo')
	fechafin = models.DateField(help_text='Fecha de fin del fondo')
	sustento = models.TextField(help_text='Sustento o referencia legal del fondo')
	activo = models.BooleanField(default=True, help_text='¿El fondo está activo?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'fer_fondos'
		verbose_name = 'Fondo FER'
		verbose_name_plural = 'Fondos FER'
		ordering = ['-ejercicio']
	
	def __str__(self):
		return f"Fondo {self.ejercicio}: ${self.fondo:,}"


class FerCatSubsidio(models.Model):
	"""Catálogo de conceptos de subsidio para FER"""
	fer_idcon = models.AutoField(primary_key=True)
	fer_descripcion = models.CharField(max_length=255, help_text='Descripción del concepto de subsidio')
	activo = models.BooleanField(default=True, help_text='¿El concepto está activo?')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	
	class Meta:
		db_table = 'fer_cat_subsidio'
		verbose_name = 'Concepto de Subsidio FER'
		verbose_name_plural = 'Conceptos de Subsidio FER'
		ordering = ['fer_idcon']
	
	def __str__(self):
		return self.fer_descripcion


class FerInformacion(models.Model):
	"""Información y registro de beneficiarios del Fondo Económico de Reserva"""
	nfer_id = models.IntegerField(primary_key=True, help_text='ID del registro FER')
	ejercicio = models.IntegerField(help_text='Año fiscal del registro')
	numcertificado = models.IntegerField(null=True, blank=True, help_text='Número de certificado')
	contrato = models.CharField(max_length=25, null=True, blank=True, help_text='Número de contrato')
	nombre = models.CharField(max_length=255, null=True, blank=True, help_text='Nombre del beneficiario')
	curp = models.CharField(max_length=18, null=True, blank=True, help_text='CURP del beneficiario')
	descripcion = models.TextField(null=True, blank=True, help_text='Descripción del concepto')
	cantidad = models.DecimalField(
		max_digits=15, decimal_places=2,
		null=True, blank=True,
		help_text='Cantidad del subsidio'
	)
	nfer_concepto = models.ForeignKey(
		FerCatSubsidio,
		on_delete=models.PROTECT,
		related_name='informaciones',
		null=True, blank=True,
		help_text='Concepto de subsidio',
		db_column='nfer_concepto_id'
	)
	fechanacimiento = models.DateField(null=True, blank=True, help_text='Fecha de nacimiento')
	domicilio = models.TextField(null=True, blank=True, help_text='Domicilio del beneficiario')
	telefono = models.CharField(max_length=20, null=True, blank=True, help_text='Teléfono del beneficiario')
	celular = models.CharField(max_length=20, null=True, blank=True, help_text='Celular del beneficiario')
	autorizo = models.CharField(max_length=255, null=True, blank=True, help_text='Persona que autorizó el subsidio')
	id_municipio = models.ForeignKey(
		CatalogosMunicipios,
		on_delete=models.PROTECT,
		related_name='fer_informaciones',
		null=True, blank=True,
		help_text='Municipio del beneficiario',
		db_column='id_municipio'
	)
	id_sexo = models.ForeignKey(
		CatalogosSexo,
		on_delete=models.PROTECT,
		related_name='fer_informaciones',
		null=True, blank=True,
		help_text='Sexo del beneficiario',
		db_column='id_sexo'
	)
	autorizo_fecha = models.DateField(null=True, blank=True, help_text='Fecha cuando se autorizó')
	autorizo_hora = models.TimeField(null=True, blank=True, help_text='Hora cuando se autorizó')
	estado = models.IntegerField(
		default=0,
		choices=[(0, 'Activo'), (1, 'Inactivo')],
		null=True, blank=True,
		help_text='Estado del registro (0=Activo, 1=Inactivo)'
	)
	parrafo_opcional = models.TextField(blank=True, null=True, help_text='Párrafo adicional opcional')
	idempmodifica = models.IntegerField(
		null=True,
		blank=True,
		help_text='ID del empleado que modificó'
	)
	fechaultimamod = models.DateField(null=True, blank=True, help_text='Fecha última modificación')
	archivo_sustento = models.CharField(
		max_length=100,
		null=True,
		blank=True,
		help_text='Archivo que sustenta la captura'
	)
	
	# Auditoría
	fecha_creacion = models.DateField(null=True, blank=True)
	fecha_modificacion_sistema = models.DateField(null=True, blank=True)
	
	class Meta:
		db_table = 'fer_informacion'
		verbose_name = 'Información FER'
		verbose_name_plural = 'Información FER'
		ordering = ['-ejercicio', '-numcertificado']
		unique_together = [['nfer_id', 'ejercicio']]
		indexes = [
			models.Index(fields=['ejercicio', 'estado']),
			models.Index(fields=['curp']),
			models.Index(fields=['estado']),
		]
	
	def __str__(self):
		return f"{self.nombre} - ${self.cantidad:,} ({self.ejercicio})" if self.nombre and self.cantidad else f"FER {self.nfer_id} ({self.ejercicio})"
# ============================================================
#  MÓDULO: TICKET DE SERVICIO
# ============================================================

class TicketServicio(models.Model):
	"""Ticket de servicio inter-departamental para agilizar pendientes"""

	PRIORIDAD_CHOICES = [
		('baja',    'Baja'),
		('normal',  'Normal'),
		('alta',    'Alta'),
		('urgente', 'Urgente'),
	]

	ESTADO_CHOICES = [
		('abierto',     'Abierto'),
		('en_proceso',  'En Proceso'),
		('en_espera',   'En Espera'),
		('resuelto',    'Resuelto'),
		('cerrado',     'Cerrado'),
	]

	CATEGORIA_CHOICES = [
		('solicitud',    'Solicitud'),
		('informacion',  'Información'),
		('soporte',      'Soporte Técnico'),
		('tramite',      'Trámite'),
		('otro',         'Otro'),
	]

	id_ticket       = models.AutoField(primary_key=True)
	folio           = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
	asunto          = models.CharField(max_length=255, help_text='Título breve del ticket')
	descripcion     = models.TextField(help_text='Descripción detallada del ticket')
	categoria       = models.CharField(max_length=30, choices=CATEGORIA_CHOICES, default='solicitud')
	prioridad       = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal')
	estado          = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='abierto')

	emisor          = models.ForeignKey(
		PersonalEmpleados, on_delete=models.PROTECT,
		related_name='tickets_enviados', help_text='Quien crea el ticket'
	)
	departamento_destino = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.PROTECT,
		related_name='tickets_recibidos_departamento',
		help_text='Departamento destino del ticket',
		null=True,
		blank=True,
	)
	receptor        = models.ForeignKey(
		PersonalEmpleados, on_delete=models.PROTECT,
		related_name='tickets_recibidos', help_text='A quien va dirigido el ticket',
		null=True,
		blank=True,
	)
	atendido_por    = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		related_name='tickets_atendidos',
		help_text='Empleado del departamento que toma el ticket',
		null=True,
		blank=True,
	)

	fecha_creacion      = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	fecha_vencimiento   = models.DateField(null=True, blank=True, help_text='Fecha límite esperada')
	fecha_resolucion    = models.DateTimeField(null=True, blank=True)

	observaciones = models.TextField(blank=True)

	class Meta:
		db_table    = 'tickets_servicio'
		verbose_name = 'Ticket de Servicio'
		verbose_name_plural = 'Tickets de Servicio'
		ordering = ['-fecha_creacion']
		indexes = [
			models.Index(fields=['estado', 'prioridad']),
			models.Index(fields=['emisor', 'departamento_destino']),
		]

	def __str__(self):
		return f"#{self.id_ticket} – {self.asunto}"

	@property
	def folio_corto(self):
		return str(self.folio).upper()[:8]

	@property
	def color_prioridad(self):
		return {
			'baja':    'secondary',
			'normal':  'info',
			'alta':    'warning',
			'urgente': 'danger',
		}.get(self.prioridad, 'secondary')

	@property
	def color_estado(self):
		return {
			'abierto':    'primary',
			'en_proceso': 'warning',
			'en_espera':  'secondary',
			'resuelto':   'success',
			'cerrado':    'dark',
		}.get(self.estado, 'secondary')

	@property
	def icono_prioridad(self):
		return {
			'baja':    'fa-arrow-down',
			'normal':  'fa-minus',
			'alta':    'fa-arrow-up',
			'urgente': 'fa-fire',
		}.get(self.prioridad, 'fa-minus')


class TicketServicioArchivo(models.Model):
	"""Archivos adjuntos de un ticket"""

	id_archivo    = models.AutoField(primary_key=True)
	ticket        = models.ForeignKey(
		TicketServicio, on_delete=models.CASCADE, related_name='archivos'
	)
	archivo       = models.FileField(upload_to='tickets/adjuntos/%Y/%m/')
	nombre_original = models.CharField(max_length=255)
	tamanio       = models.PositiveIntegerField(default=0, help_text='Tamaño en bytes')
	tipo_mime     = models.CharField(max_length=100, blank=True)
	subido_por    = models.ForeignKey(
		PersonalEmpleados, on_delete=models.SET_NULL, null=True,
		related_name='archivos_tickets'
	)
	fecha_subida  = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'tickets_servicio_archivo'
		verbose_name = 'Archivo de Ticket'
		verbose_name_plural = 'Archivos de Tickets'
		ordering = ['fecha_subida']

	def __str__(self):
		return self.nombre_original

	@property
	def tamanio_legible(self):
		size = self.tamanio
		for unit in ['B', 'KB', 'MB', 'GB']:
			if size < 1024:
				return f"{size:.1f} {unit}"
			size /= 1024
		return f"{size:.1f} TB"

	@property
	def es_imagen(self):
		return self.tipo_mime.startswith('image/') if self.tipo_mime else False

	@property
	def icono(self):
		mime = self.tipo_mime or ''
		if 'pdf' in mime:             return 'fa-file-pdf text-danger'
		if 'word' in mime or 'doc' in self.nombre_original.lower(): return 'fa-file-word text-primary'
		if 'excel' in mime or 'xls' in self.nombre_original.lower(): return 'fa-file-excel text-success'
		if mime.startswith('image/'): return 'fa-file-image text-warning'
		if 'zip' in mime or 'rar' in mime: return 'fa-file-archive text-secondary'
		return 'fa-file text-muted'


class TicketServicioComentario(models.Model):
	"""Comentarios y actualizaciones del ticket"""

	id_comentario = models.AutoField(primary_key=True)
	ticket        = models.ForeignKey(
		TicketServicio, on_delete=models.CASCADE, related_name='comentarios'
	)
	autor         = models.ForeignKey(
		PersonalEmpleados, on_delete=models.SET_NULL, null=True,
		related_name='comentarios_tickets'
	)
	mensaje       = models.TextField()
	es_nota_interna = models.BooleanField(default=False, help_text='Solo visible para el emisor del ticket')
	cambio_estado   = models.CharField(max_length=15, blank=True, help_text='Estado anterior si hubo cambio')
	fecha           = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'tickets_servicio_comentario'
		verbose_name = 'Comentario de Ticket'
		verbose_name_plural = 'Comentarios de Tickets'
		ordering = ['fecha']

	def __str__(self):
		return f"Ticket #{self.ticket.id_ticket} – {self.autor}"


class TicketMantenimiento(models.Model):
	"""Tickets para atención de equipo y soporte de mantenimiento."""

	SLA_HORAS_POR_PRIORIDAD = {
		'baja': 72,
		'normal': 48,
		'alta': 24,
		'critica': 8,
	}

	TIPO_EQUIPO_CHOICES = [
		('desktop', 'Computadora de escritorio'),
		('laptop', 'Laptop'),
		('impresora', 'Impresora'),
		('scanner', 'Escáner'),
		('red', 'Red / Internet'),
		('periferico', 'Periférico'),
		('otro', 'Otro'),
	]

	PRIORIDAD_CHOICES = [
		('baja', 'Baja'),
		('normal', 'Normal'),
		('alta', 'Alta'),
		('critica', 'Crítica'),
	]

	ESTADO_CHOICES = [
		('abierto', 'Abierto'),
		('asignado', 'Asignado'),
		('en_revision', 'En revisión'),
		('en_reparacion', 'En reparación'),
		('espera_refaccion', 'En espera de refacción'),
		('resuelto', 'Resuelto'),
		('entregado', 'Entregado'),
		('cerrado', 'Cerrado'),
	]

	id_ticket_mantenimiento = models.AutoField(primary_key=True)
	folio = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
	asunto = models.CharField(max_length=255, help_text='Título breve de la incidencia')
	descripcion = models.TextField(help_text='Descripción del problema reportado')
	tipo_equipo = models.CharField(max_length=20, choices=TIPO_EQUIPO_CHOICES, default='desktop')
	equipo = models.CharField(max_length=150, blank=True, help_text='Nombre o referencia del equipo')
	numero_inventario = models.CharField(max_length=100, blank=True, help_text='Número de inventario o serie')
	ubicacion = models.CharField(max_length=255, blank=True, help_text='Ubicación exacta del equipo o del solicitante')
	prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='normal')
	estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='abierto')

	solicitante = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.PROTECT,
		related_name='tickets_mantenimiento_solicitados',
		help_text='Empleado que reporta la incidencia'
	)
	departamento_solicitante = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='tickets_mantenimiento_solicitados',
		help_text='Departamento del empleado solicitante'
	)
	departamento_soporte = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.PROTECT,
		related_name='tickets_mantenimiento_recibidos',
		help_text='Departamento responsable de la atención'
	)
	atendido_por = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='tickets_mantenimiento_atendidos',
		help_text='Empleado del área de soporte que atiende el ticket'
	)

	solicita_formateo = models.BooleanField(default=False)
	equipo_retirado = models.BooleanField(default=False)
	trabajo_realizado = models.TextField(blank=True)
	piezas_instaladas = models.TextField(blank=True)
	sla_horas_objetivo = models.PositiveIntegerField(default=48)
	fecha_limite_sla = models.DateTimeField(null=True, blank=True)
	fecha_retiro_equipo = models.DateTimeField(null=True, blank=True)
	fecha_resolucion = models.DateTimeField(null=True, blank=True)
	fecha_entrega_equipo = models.DateTimeField(null=True, blank=True)
	solucion_confirmada = models.BooleanField(default=False)

	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'tickets_mantenimiento'
		verbose_name = 'Ticket de Mantenimiento'
		verbose_name_plural = 'Tickets de Mantenimiento'
		ordering = ['-fecha_creacion']
		indexes = [
			models.Index(fields=['estado', 'prioridad']),
			models.Index(fields=['solicitante', 'departamento_soporte']),
		]

	def __str__(self):
		return f"MTTO #{self.id_ticket_mantenimiento} – {self.asunto}"

	@property
	def folio_corto(self):
		return str(self.folio).upper()[:8]

	@property
	def color_prioridad(self):
		return {
			'baja': 'secondary',
			'normal': 'info',
			'alta': 'warning',
			'critica': 'danger',
		}.get(self.prioridad, 'secondary')

	@property
	def color_estado(self):
		return {
			'abierto': 'primary',
			'asignado': 'info',
			'en_revision': 'warning',
			'en_reparacion': 'warning',
			'espera_refaccion': 'secondary',
			'resuelto': 'success',
			'entregado': 'success',
			'cerrado': 'dark',
		}.get(self.estado, 'secondary')

	@property
	def icono_prioridad(self):
		return {
			'baja': 'fa-arrow-down',
			'normal': 'fa-minus',
			'alta': 'fa-arrow-up',
			'critica': 'fa-bolt',
		}.get(self.prioridad, 'fa-minus')

	@property
	def esta_vencido(self):
		if not self.fecha_limite_sla:
			return False
		if self.estado in ['resuelto', 'entregado', 'cerrado']:
			return False
		return timezone.now() > self.fecha_limite_sla

	@property
	def horas_restantes_sla(self):
		if not self.fecha_limite_sla:
			return None
		delta = self.fecha_limite_sla - timezone.now()
		return int(delta.total_seconds() // 3600)


class TicketMantenimientoArchivo(models.Model):
	"""Archivos adjuntos de tickets de mantenimiento."""

	id_archivo = models.AutoField(primary_key=True)
	ticket = models.ForeignKey(
		TicketMantenimiento, on_delete=models.CASCADE, related_name='archivos'
	)
	archivo = models.FileField(upload_to='mantenimiento/adjuntos/%Y/%m/')
	nombre_original = models.CharField(max_length=255)
	tamanio = models.PositiveIntegerField(default=0)
	tipo_mime = models.CharField(max_length=100, blank=True)
	subido_por = models.ForeignKey(
		PersonalEmpleados, on_delete=models.SET_NULL, null=True,
		related_name='archivos_tickets_mantenimiento'
	)
	fecha_subida = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'tickets_mantenimiento_archivo'
		verbose_name = 'Archivo de Ticket de Mantenimiento'
		verbose_name_plural = 'Archivos de Tickets de Mantenimiento'
		ordering = ['fecha_subida']

	def __str__(self):
		return self.nombre_original

	@property
	def tamanio_legible(self):
		size = self.tamanio
		for unit in ['B', 'KB', 'MB', 'GB']:
			if size < 1024:
				return f"{size:.1f} {unit}"
			size /= 1024
		return f"{size:.1f} TB"

	@property
	def icono(self):
		mime = self.tipo_mime or ''
		if 'pdf' in mime:
			return 'fa-file-pdf text-danger'
		if 'word' in mime or 'doc' in self.nombre_original.lower():
			return 'fa-file-word text-primary'
		if 'excel' in mime or 'xls' in self.nombre_original.lower():
			return 'fa-file-excel text-success'
		if mime.startswith('image/'):
			return 'fa-file-image text-warning'
		if 'zip' in mime or 'rar' in mime:
			return 'fa-file-archive text-secondary'
		return 'fa-file text-muted'


class TicketMantenimientoSeguimiento(models.Model):
	"""Bitácora y comentarios de atención de mantenimiento."""

	TIPO_CHOICES = [
		('comentario', 'Comentario'),
		('estado', 'Cambio de estado'),
		('intervencion', 'Intervención técnica'),
		('notificacion', 'Notificación'),
	]

	id_seguimiento = models.AutoField(primary_key=True)
	ticket = models.ForeignKey(
		TicketMantenimiento, on_delete=models.CASCADE, related_name='seguimientos'
	)
	autor = models.ForeignKey(
		PersonalEmpleados, on_delete=models.SET_NULL, null=True,
		related_name='seguimientos_tickets_mantenimiento'
	)
	tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='comentario')
	mensaje = models.TextField()
	trabajo_realizado = models.TextField(blank=True)
	piezas_instaladas = models.TextField(blank=True)
	cambio_estado = models.CharField(max_length=20, blank=True)
	notificar_solicitante = models.BooleanField(default=False)
	fecha = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'tickets_mantenimiento_seguimiento'
		verbose_name = 'Seguimiento de Ticket de Mantenimiento'
		verbose_name_plural = 'Seguimientos de Tickets de Mantenimiento'
		ordering = ['fecha']

	def __str__(self):
		return f"MTTO #{self.ticket.id_ticket_mantenimiento} – {self.tipo}"


class RequisicionesClasificacion(models.Model):
	id_clasificacion = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=120, unique=True)
	descripcion = models.TextField(blank=True)
	activo = models.BooleanField(default=True)
	fecha_captura = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'requisiciones_clasificaciones'
		verbose_name = 'Clasificación de Artículo'
		verbose_name_plural = 'Clasificaciones de Artículos'
		ordering = ['nombre']

	def __str__(self):
		return self.nombre


class RequisicionesCatalogoArticulos(models.Model):
	UNIDAD_MEDIDA_CHOICES = [
		('pieza', 'Pieza'),
		('caja', 'Caja'),
		('paquete', 'Paquete'),
	]

	id_articulo = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=200)
	clasificacion = models.ForeignKey(
		RequisicionesClasificacion,
		on_delete=models.PROTECT,
		related_name='articulos'
	)
	descripcion = models.TextField(blank=True)
	unidad_medida = models.CharField(max_length=20, choices=UNIDAD_MEDIDA_CHOICES, default='pieza')
	stock_actual = models.PositiveIntegerField(default=0)
	precio_referencia = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	imagen = models.ImageField(upload_to='requisiciones/articulos/', null=True, blank=True)
	activo = models.BooleanField(default=True)
	fecha_captura = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	usuario_captura = models.CharField(max_length=100, blank=True)
	usuario_modificacion = models.CharField(max_length=100, blank=True)

	class Meta:
		db_table = 'requisiciones_catalogodearticulos'
		verbose_name = 'Artículo de Requisiciones'
		verbose_name_plural = 'Catálogo de Artículos para Requisiciones'
		ordering = ['nombre']
		indexes = [
			models.Index(fields=['activo', 'nombre']),
		]

	def __str__(self):
		return self.nombre


class RequisicionesSolicitud(models.Model):
	ESTATUS_CHOICES = [
		('pendiente', 'Pendiente de atender'),
		('en_proceso', 'En proceso'),
		('para_entrega', 'Para entrega'),
		('no_autorizado', 'No autorizado'),
		('entregado', 'Entregado'),
	]

	id_requisicion = models.AutoField(primary_key=True)
	folio = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True)
	solicitante = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.PROTECT,
		related_name='requisiciones_solicitadas'
	)
	departamento_solicitante = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='requisiciones_solicitadas'
	)
	departamento_atencion = models.ForeignKey(
		PersonalDepartamento,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='requisiciones_recibidas'
	)
	atendido_por = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='requisiciones_atendidas'
	)
	recibido_por = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='requisiciones_recibidas_empleado'
	)
	estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default='pendiente')
	comentarios_compra = models.TextField(blank=True)
	no_autorizado_motivo = models.TextField(blank=True)
	fecha_toma = models.DateTimeField(null=True, blank=True)
	fecha_para_entrega = models.DateTimeField(null=True, blank=True)
	fecha_entrega = models.DateTimeField(null=True, blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'requisiciones_solicitudes'
		verbose_name = 'Requisición'
		verbose_name_plural = 'Requisiciones'
		ordering = ['-fecha_creacion']
		indexes = [
			models.Index(fields=['estatus', 'fecha_creacion']),
			models.Index(fields=['departamento_solicitante', 'estatus']),
		]

	def __str__(self):
		return f"REQ #{self.id_requisicion} – {self.solicitante.nombre_completo}"

	@property
	def folio_corto(self):
		return str(self.folio).upper()[:8]

	@property
	def total_estimado(self):
		return sum(detalle.subtotal for detalle in self.detalles.all())

	@property
	def total_entregado(self):
		return sum(detalle.subtotal_entregado for detalle in self.detalles.all())


class RequisicionesSolicitudDetalle(models.Model):
	ESTATUS_DETALLE_CHOICES = [
		('pendiente', 'Pendiente'),
		('parcial', 'Parcial'),
		('no_autorizado', 'No autorizado'),
		('para_entrega', 'Para entrega'),
		('entregado', 'Entregado'),
	]

	id_detalle = models.AutoField(primary_key=True)
	requisicion = models.ForeignKey(
		RequisicionesSolicitud,
		on_delete=models.CASCADE,
		related_name='detalles'
	)
	articulo = models.ForeignKey(
		RequisicionesCatalogoArticulos,
		on_delete=models.PROTECT,
		related_name='detalles_requisicion'
	)
	motivo = models.TextField(help_text='Justificación, descripción o motivo de solicitud')
	cantidad_solicitada = models.PositiveIntegerField(validators=[MinValueValidator(1)])
	unidad_medida = models.CharField(max_length=20, choices=RequisicionesCatalogoArticulos.UNIDAD_MEDIDA_CHOICES, default='pieza')
	cantidad_autorizada = models.PositiveIntegerField(default=0)
	cantidad_entregada = models.PositiveIntegerField(default=0)
	costo_unitario = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	estatus_detalle = models.CharField(max_length=20, choices=ESTATUS_DETALLE_CHOICES, default='pendiente')
	observaciones_compra = models.TextField(blank=True)

	class Meta:
		db_table = 'requisiciones_detalle'
		verbose_name = 'Detalle de Requisición'
		verbose_name_plural = 'Detalles de Requisición'
		ordering = ['id_detalle']

	def __str__(self):
		return f"{self.requisicion_id} - {self.articulo.nombre}"

	@property
	def subtotal(self):
		return self.cantidad_autorizada * self.costo_unitario

	@property
	def subtotal_entregado(self):
		return self.cantidad_entregada * self.costo_unitario


class RequisicionesDocumento(models.Model):
	TIPO_DOCUMENTO_CHOICES = [
		('cotizacion', 'Cotización'),
		('factura', 'Factura'),
	]

	id_documento = models.AutoField(primary_key=True)
	requisicion = models.ForeignKey(
		RequisicionesSolicitud,
		on_delete=models.CASCADE,
		related_name='documentos'
	)
	detalle = models.ForeignKey(
		RequisicionesSolicitudDetalle,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='documentos'
	)
	tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
	archivo = models.FileField(upload_to='requisiciones/documentos/%Y/%m/')
	nombre_original = models.CharField(max_length=255)
	proveedor = models.CharField(max_length=200, blank=True)
	descripcion = models.CharField(max_length=255, blank=True)
	subido_por = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='documentos_requisiciones_subidos'
	)
	fecha_subida = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'requisiciones_documentos'
		verbose_name = 'Documento de Requisición'
		verbose_name_plural = 'Documentos de Requisiciones'
		ordering = ['-fecha_subida']

	def __str__(self):
		return self.nombre_original

	@property
	def es_pdf(self):
		return self.nombre_original.lower().endswith('.pdf')


class RequisicionesSeguimiento(models.Model):
	TIPO_CHOICES = [
		('estado', 'Cambio de estado'),
		('comentario', 'Comentario'),
		('documento', 'Documento'),
		('entrega', 'Entrega'),
	]

	id_seguimiento = models.AutoField(primary_key=True)
	requisicion = models.ForeignKey(
		RequisicionesSolicitud,
		on_delete=models.CASCADE,
		related_name='seguimientos'
	)
	autor = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='seguimientos_requisiciones'
	)
	tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='comentario')
	mensaje = models.TextField()
	estatus_anterior = models.CharField(max_length=20, blank=True)
	estatus_nuevo = models.CharField(max_length=20, blank=True)
	fecha = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'requisiciones_seguimiento'
		verbose_name = 'Seguimiento de Requisición'
		verbose_name_plural = 'Seguimientos de Requisiciones'
		ordering = ['fecha']

	def __str__(self):
		return f"REQ #{self.requisicion_id} – {self.tipo}"


# ==================== MODELOS DE VEHICULOS ====================

class VehiculosMarcas(models.Model):
	clave_marca = models.IntegerField(primary_key=True, db_column='Clave_Marca')
	marca = models.CharField(max_length=255, db_column='Marca', blank=True)

	class Meta:
		db_table = 'vehiculos_marcas'
		verbose_name = 'Marca de Vehiculo'
		verbose_name_plural = 'Marcas de Vehiculos'
		ordering = ['clave_marca']

	def __str__(self):
		return self.marca or str(self.clave_marca)


class VehiculosColores(models.Model):
	clave_color = models.IntegerField(primary_key=True, db_column='Clave_Color')
	color = models.CharField(max_length=255, db_column='Color', blank=True)

	class Meta:
		db_table = 'vehiculos_colores'
		verbose_name = 'Color de Vehiculo'
		verbose_name_plural = 'Colores de Vehiculos'
		ordering = ['clave_color']

	def __str__(self):
		return self.color or str(self.clave_color)


class VehiculosEstatus(models.Model):
	idestatus = models.IntegerField(primary_key=True, db_column='IdEstatus')
	estatus = models.CharField(max_length=255, db_column='Estatus')

	class Meta:
		db_table = 'vehiculos_estatus'
		verbose_name = 'Estatus de Vehiculo'
		verbose_name_plural = 'Estatus de Vehiculos'
		ordering = ['idestatus']

	def __str__(self):
		return self.estatus


class VehiculoPropietario(models.Model):
	idpropietario = models.IntegerField(primary_key=True, db_column='IdPropietario')
	propietario = models.CharField(max_length=255, db_column='Propietario', blank=True)

	class Meta:
		db_table = 'vehiculo_propietario'
		verbose_name = 'Propietario de Vehiculo'
		verbose_name_plural = 'Propietarios de Vehiculos'
		ordering = ['idpropietario']

	def __str__(self):
		return self.propietario or str(self.idpropietario)


class VehiculosTiposDeMantenimiento(models.Model):
	clave_tipo_mant = models.IntegerField(primary_key=True, db_column='clave_tipo_mant')
	tipo_mantenimiento = models.CharField(max_length=255, db_column='Tipo_Mantenimiento', blank=True)

	class Meta:
		db_table = 'vehiculos_tiposdemantenimiento'
		verbose_name = 'Tipo de Mantenimiento'
		verbose_name_plural = 'Tipos de Mantenimiento'
		ordering = ['clave_tipo_mant']

	def __str__(self):
		return self.tipo_mantenimiento or str(self.clave_tipo_mant)


class VehiculosProveedores(models.Model):
	clave_proveedor = models.IntegerField(primary_key=True, db_column='clave_proveedor')
	nombre_proveedor = models.CharField(max_length=255, db_column='Nombre_proveedor', blank=True)

	class Meta:
		db_table = 'vehiculos_proveedores'
		verbose_name = 'Proveedor de Vehiculos'
		verbose_name_plural = 'Proveedores de Vehiculos'
		ordering = ['clave_proveedor']

	def __str__(self):
		return self.nombre_proveedor or str(self.clave_proveedor)


class Vehiculos(models.Model):
	num_economico = models.CharField(max_length=255, primary_key=True, db_column='Num_economico')
	clave_marca = models.ForeignKey(VehiculosMarcas, on_delete=models.SET_NULL, null=True, blank=True, db_column='Clave_marca')
	tipo = models.CharField(max_length=255, db_column='Tipo', blank=True)
	clave_color = models.ForeignKey(VehiculosColores, on_delete=models.SET_NULL, null=True, blank=True, db_column='Clave_Color')
	modelo = models.IntegerField(db_column='Modelo', null=True, blank=True)
	placas = models.CharField(max_length=255, db_column='Placas', blank=True)
	serie = models.CharField(max_length=255, db_column='Serie', blank=True)
	idestatus = models.ForeignKey(VehiculosEstatus, on_delete=models.RESTRICT, db_column='IdEstatus')
	idareaadscripcion = models.ForeignKey(PersonalDepartamento, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdAreaAdscripcion')
	idresguradante = models.ForeignKey(PersonalEmpleados, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdResguradante')
	comentario = models.TextField(db_column='Comentario', blank=True)
	cilindros = models.IntegerField(db_column='Cilindros')
	idpropietario = models.ForeignKey(VehiculoPropietario, on_delete=models.SET_NULL, null=True, blank=True, db_column='IdPropietario')

	class Meta:
		db_table = 'vehiculos'
		verbose_name = 'Vehiculo'
		verbose_name_plural = 'Vehiculos'
		ordering = ['num_economico']

	def __str__(self):
		return self.num_economico


class VehiculosBitacora(models.Model):
	clave_servicio = models.AutoField(primary_key=True, db_column='Clave_servicio')
	num_economico = models.ForeignKey(Vehiculos, on_delete=models.RESTRICT, db_column='Num_economico')
	fecha_solicitud = models.DateTimeField(db_column='Fecha_solicitud')
	fecha_ejecucion = models.DateTimeField(db_column='Fecha_ejecucion')
	clave_tipo_mant = models.ForeignKey(VehiculosTiposDeMantenimiento, on_delete=models.RESTRICT, db_column='clave_tipo_mant')
	km_prog = models.IntegerField(db_column='Km_prog')
	km_real = models.IntegerField(db_column='Km_real')
	num_solicitud = models.IntegerField(db_column='num_solicitud')
	num_factura = models.CharField(max_length=255, db_column='num_factura')
	clave_proveedor = models.ForeignKey(VehiculosProveedores, on_delete=models.RESTRICT, db_column='clave_proveedor')
	descripcion = models.CharField(max_length=1000, db_column='Descripcion')
	costo_mano_obra = models.DecimalField(max_digits=19, decimal_places=4, db_column='Costo_mano_obra')
	costo_refaccion = models.DecimalField(max_digits=19, decimal_places=4, db_column='Costo_refaccion')
	importe_factura = models.DecimalField(max_digits=19, decimal_places=4, db_column='Importe_factura')
	archivo_factura = models.FileField(upload_to='vehiculos/facturas/', db_column='Archivo_factura', null=True, blank=True)
	cancelada = models.BooleanField(db_column='Cancelada', default=False)
	act_fecha = models.DateField(db_column='act_fecha')
	act_hora = models.TimeField(db_column='act_hora')
	act_user = models.CharField(max_length=50, db_column='act_user')

	class Meta:
		db_table = 'vehiculos_bitacora'
		verbose_name = 'Bitacora de Vehiculo'
		verbose_name_plural = 'Bitacora de Vehiculos'
		ordering = ['-clave_servicio']

	def __str__(self):
		return f"Servicio #{self.clave_servicio} - {self.num_economico_id}"


class VehiculoFoto(models.Model):
	idfoto = models.AutoField(primary_key=True)
	vehiculo = models.ForeignKey(Vehiculos, on_delete=models.CASCADE, related_name='fotos')
	imagen = models.ImageField(upload_to='vehiculos/fotos/')
	descripcion = models.CharField(max_length=255, blank=True)
	es_principal = models.BooleanField(default=False)
	orden = models.PositiveIntegerField(default=0)
	fecha_captura = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'vehiculo_fotos'
		verbose_name = 'Foto de Vehiculo'
		verbose_name_plural = 'Fotos de Vehiculos'
		ordering = ['-es_principal', 'orden', '-fecha_captura']

	def __str__(self):
		return f"Foto {self.idfoto} - {self.vehiculo_id}"


class ViaticosZonaTarifa(models.Model):
	ZONA_NORTE = 'norte'
	ZONA_CENTRO = 'centro'
	ZONA_SUR = 'sur'

	ZONA_CHOICES = [
		(ZONA_NORTE, 'Norte'),
		(ZONA_CENTRO, 'Centro'),
		(ZONA_SUR, 'Sur'),
	]

	clave = models.CharField(max_length=20, choices=ZONA_CHOICES, unique=True)
	nombre = models.CharField(max_length=50)
	hospedaje_noche = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	alimentacion_diaria = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	combustible_km = models.DecimalField(max_digits=12, decimal_places=4, default=0)
	activo = models.BooleanField(default=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'viaticos_zona_tarifa'
		verbose_name = 'Tarifa de Zona de Viaticos'
		verbose_name_plural = 'Tarifas de Zonas de Viaticos'
		ordering = ['clave']

	def __str__(self):
		return self.nombre


class ViaticosPresupuestoDireccion(models.Model):
	iddireccion = models.ForeignKey(
		PersonalDireccion,
		on_delete=models.CASCADE,
		related_name='presupuestos_viaticos'
	)
	ejercicio = models.PositiveIntegerField(default=_current_year)
	monto_asignado = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0)])
	activo = models.BooleanField(default=True)
	observaciones = models.TextField(blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'viaticos_presupuesto_direccion'
		verbose_name = 'Presupuesto de Viaticos por Direccion'
		verbose_name_plural = 'Presupuestos de Viaticos por Direccion'
		ordering = ['-ejercicio', 'iddireccion__direccion']
		unique_together = ('iddireccion', 'ejercicio')

	def __str__(self):
		return f"{self.iddireccion} - {self.ejercicio}"

	def monto_comprometido(self, excluir_solicitud_id=None):
		queryset = self.solicitudes.filter(estatus__in=[ViaticosSolicitud.ESTATUS_CAPTURADO, ViaticosSolicitud.ESTATUS_AUTORIZADO])
		if excluir_solicitud_id:
			queryset = queryset.exclude(pk=excluir_solicitud_id)
		resultado = queryset.aggregate(total=models.Sum('total_estimado'))
		return resultado.get('total') or Decimal('0.00')

	def monto_disponible(self, excluir_solicitud_id=None):
		disponible = self.monto_asignado - self.monto_comprometido(excluir_solicitud_id=excluir_solicitud_id)
		return disponible.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


class ViaticosSolicitud(models.Model):
	TRANSPORTE_VEHICULO = 'vehiculo_interno'
	TRANSPORTE_AUTOBUS = 'autobus'
	TRANSPORTE_AVION = 'avion'
	TRANSPORTE_MIXTO = 'mixto'

	TRANSPORTE_CHOICES = [
		(TRANSPORTE_VEHICULO, 'Vehiculo interno'),
		(TRANSPORTE_AUTOBUS, 'Autobus'),
		(TRANSPORTE_AVION, 'Avion'),
		(TRANSPORTE_MIXTO, 'Mixto'),
	]

	ESTATUS_CAPTURADO = 'capturado'
	ESTATUS_AUTORIZADO = 'autorizado'
	ESTATUS_CANCELADO = 'cancelado'

	ESTATUS_CHOICES = [
		(ESTATUS_CAPTURADO, 'Capturado'),
		(ESTATUS_AUTORIZADO, 'Autorizado'),
		(ESTATUS_CANCELADO, 'Cancelado'),
	]

	folio = models.CharField(max_length=30, unique=True, blank=True)
	empleado = models.ForeignKey(PersonalEmpleados, on_delete=models.PROTECT, related_name='viaticos')
	direccion = models.ForeignKey(
		PersonalDireccion,
		on_delete=models.PROTECT,
		related_name='solicitudes_viaticos'
	)
	presupuesto = models.ForeignKey(
		ViaticosPresupuestoDireccion,
		on_delete=models.PROTECT,
		related_name='solicitudes'
	)
	zona = models.ForeignKey(ViaticosZonaTarifa, on_delete=models.PROTECT, related_name='solicitudes')
	motivo_comision = models.TextField()
	origen = models.CharField(max_length=255)
	destino = models.CharField(max_length=255)
	origen_latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	origen_longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	destino_latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	destino_longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	distancia_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	viaje_redondo = models.BooleanField(default=True)
	dias = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
	transporte = models.CharField(max_length=20, choices=TRANSPORTE_CHOICES, default=TRANSPORTE_VEHICULO)
	pasajes_estimados = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	taxis_estimados = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	combustible_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	hospedaje_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	alimentacion_estimada = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	total_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ESTATUS_CAPTURADO)
	seguimiento_activo = models.BooleanField(default=False)
	ultima_latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	ultima_longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
	ultima_precision_metros = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	ultima_velocidad_kmh = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	ultima_actualizacion_ubicacion = models.DateTimeField(null=True, blank=True)
	observaciones = models.TextField(blank=True)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)
	creado_por = models.ForeignKey(
		PersonalEmpleados,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='viaticos_capturados'
	)

	class Meta:
		db_table = 'viaticos_solicitud'
		verbose_name = 'Solicitud de Viaticos'
		verbose_name_plural = 'Solicitudes de Viaticos'
		ordering = ['-fecha_creacion', '-id']

	def __str__(self):
		return self.folio or f"Viaticos #{self.pk}"

	@staticmethod
	def _money(valor):
		return Decimal(valor or 0).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

	def _calcular_hospedaje(self):
		noches = max(int(self.dias or 0) - 1, 0)
		return self._money(noches * Decimal(self.zona.hospedaje_noche or 0))

	def _calcular_alimentacion(self):
		return self._money(int(self.dias or 0) * Decimal(self.zona.alimentacion_diaria or 0))

	def _calcular_combustible(self):
		if self.transporte not in [self.TRANSPORTE_VEHICULO, self.TRANSPORTE_MIXTO]:
			return Decimal('0.00')
		factor = Decimal('2') if self.viaje_redondo else Decimal('1')
		distancia_total = Decimal(self.distancia_km or 0) * factor
		return self._money(distancia_total * Decimal(self.zona.combustible_km or 0))

	def recalcular_totales(self):
		self.hospedaje_estimado = self._calcular_hospedaje()
		self.alimentacion_estimada = self._calcular_alimentacion()
		self.combustible_estimado = self._calcular_combustible()
		pasajes = self._money(self.pasajes_estimados)
		taxis = self._money(self.taxis_estimados)
		self.total_estimado = self._money(
			Decimal(self.hospedaje_estimado or 0)
			+ Decimal(self.alimentacion_estimada or 0)
			+ Decimal(self.combustible_estimado or 0)
			+ pasajes
			+ taxis
		)

	def clean(self):
		errores = {}

		if self.empleado_id:
			departamento = getattr(self.empleado, 'iddepartamento', None)
			direccion_empleado = getattr(departamento, 'iddireccion', None)
			if direccion_empleado is None:
				errores['empleado'] = 'El empleado seleccionado no tiene direccion asignada por departamento.'
			elif self.direccion_id and self.direccion_id != direccion_empleado.iddireccion:
				errores['empleado'] = 'La direccion del viatico debe coincidir con la direccion del empleado.'
			else:
				self.direccion = direccion_empleado

		if self.presupuesto_id and self.direccion_id and self.presupuesto.iddireccion_id != self.direccion_id:
			errores['presupuesto'] = 'El presupuesto seleccionado no corresponde a la direccion del empleado.'

		if self.dias and self.dias < 1:
			errores['dias'] = 'Los dias deben ser al menos 1.'

		if self.transporte == self.TRANSPORTE_VEHICULO:
			self.pasajes_estimados = Decimal('0.00')

		self.recalcular_totales()

		if self.presupuesto_id and self.estatus != self.ESTATUS_CANCELADO:
			disponible = self.presupuesto.monto_disponible(excluir_solicitud_id=self.pk)
			if self.total_estimado > disponible:
				errores['__all__'] = (
					f'El viatico excede el presupuesto disponible de la direccion. '
					f'Disponible: ${disponible}.'
				)

		if errores:
			raise ValidationError(errores)

	def save(self, *args, **kwargs):
		self.full_clean()
		if not self.folio:
			year = timezone.localdate().year
			ultimo = ViaticosSolicitud.objects.filter(folio__startswith=f'VIA-{year}-').count() + 1
			self.folio = f'VIA-{year}-{ultimo:04d}'
		return super().save(*args, **kwargs)

	def registrar_ubicacion(self, empleado, latitud, longitud, precision_metros=None, velocidad_kmh=None, fuente='navegador'):
		if self.estatus == self.ESTATUS_CANCELADO:
			raise ValidationError('No se puede registrar ubicacion en un viatico cancelado.')

		ubicacion = ViaticosUbicacion.objects.create(
			viatico=self,
			empleado=empleado,
			latitud=latitud,
			longitud=longitud,
			precision_metros=precision_metros,
			velocidad_kmh=velocidad_kmh,
			fuente=fuente,
		)
		self.seguimiento_activo = True
		self.ultima_latitud = latitud
		self.ultima_longitud = longitud
		self.ultima_precision_metros = precision_metros
		self.ultima_velocidad_kmh = velocidad_kmh
		self.ultima_actualizacion_ubicacion = ubicacion.fecha_reporte
		super().save(update_fields=[
			'seguimiento_activo',
			'ultima_latitud',
			'ultima_longitud',
			'ultima_precision_metros',
			'ultima_velocidad_kmh',
			'ultima_actualizacion_ubicacion',
			'fecha_modificacion',
		])
		return ubicacion


class ViaticosUbicacion(models.Model):
	FUENTE_NAVEGADOR = 'navegador'
	FUENTE_MANUAL = 'manual'

	FUENTE_CHOICES = [
		(FUENTE_NAVEGADOR, 'Navegador'),
		(FUENTE_MANUAL, 'Manual'),
	]

	viatico = models.ForeignKey(ViaticosSolicitud, on_delete=models.CASCADE, related_name='ubicaciones')
	empleado = models.ForeignKey(PersonalEmpleados, on_delete=models.CASCADE, related_name='ubicaciones_viaticos')
	latitud = models.DecimalField(max_digits=9, decimal_places=6)
	longitud = models.DecimalField(max_digits=9, decimal_places=6)
	precision_metros = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	velocidad_kmh = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
	fuente = models.CharField(max_length=20, choices=FUENTE_CHOICES, default=FUENTE_NAVEGADOR)
	fecha_reporte = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'viaticos_ubicacion'
		verbose_name = 'Ubicacion de Viaticos'
		verbose_name_plural = 'Ubicaciones de Viaticos'
		ordering = ['-fecha_reporte', '-id']

	def __str__(self):
		return f"{self.viatico.folio} @ {self.fecha_reporte:%Y-%m-%d %H:%M:%S}"
