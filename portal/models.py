from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from django.core.validators import MinValueValidator, MaxValueValidator


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