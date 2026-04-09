from django.contrib import admin

from .models import (
	Anuncio,
	SeguridadContactanos,
	CatalogosEntidadesFederativas,
	CatalogosMunicipios,
	SeguridadConfiguracionDelSistema,
	CatalogosDelegaciones,
	PersonalDireccion,
	PersonalDepartamento,
	PersonalTipoDeContratacion,
	PersonalPuestos,
	PersonalEmpleados,
	RecuperacionContrasena,
	ConfiguracionSistema,
	UsuariosDelSistema,
	ColaCorreos,
	TicketMantenimiento,
	TicketMantenimientoArchivo,
	TicketMantenimientoSeguimiento,
	RequisicionesClasificacion,
	RequisicionesCatalogoArticulos,
	RequisicionesSolicitud,
	RequisicionesSolicitudDetalle,
	RequisicionesDocumento,
	RequisicionesSeguimiento,
)

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
	list_display = ("titulo", "fecha_publicacion", "activo")


@admin.register(SeguridadContactanos)
class SeguridadContactanosAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'nombre_completo',
		'email',
		'compania_organizacion',
		'leido_badge',
		'fecha_hora_insercion',
	)
	search_fields = ('nombre_completo', 'email', 'compania_organizacion', 'asunto')
	list_filter = ('leido', 'fecha_hora_insercion')
	readonly_fields = ('fecha_hora_insercion', 'ip_origen', 'user_agent', 'fecha_lectura')
	actions = ('marcar_como_leido', 'marcar_como_no_leido')

	def leido_badge(self, obj):
		if obj.leido:
			return '<span style="color: green; font-weight: bold;">✓ Leído</span>'
		else:
			return '<span style="color: red; font-weight: bold;">✗ No leído</span>'
	leido_badge.short_description = 'Estado de lectura'
	leido_badge.allow_tags = True

	def marcar_como_leido(self, request, queryset):
		from django.utils import timezone
		queryset.update(leido=True, fecha_lectura=timezone.now())
		self.message_user(request, 'Mensaje(s) marcado(s) como leído(s).')
	marcar_como_leido.short_description = 'Marcar como leído'

	def marcar_como_no_leido(self, request, queryset):
		queryset.update(leido=False, fecha_lectura=None)
		self.message_user(request, 'Mensaje(s) marcado(s) como no leído(s).')
	marcar_como_no_leido.short_description = 'Marcar como no leído'


@admin.register(CatalogosEntidadesFederativas)
class CatalogosEntidadesFederativasAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'clave')
	search_fields = ('nombre', 'clave')
	ordering = ('nombre',)


@admin.register(CatalogosMunicipios)
class CatalogosMunicipiosAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'entidad', 'clave')
	search_fields = ('nombre', 'entidad__nombre')
	list_filter = ('entidad',)
	ordering = ('entidad', 'nombre')


@admin.register(SeguridadConfiguracionDelSistema)
class SeguridadConfiguracionDelSistemaAdmin(admin.ModelAdmin):
	list_display = ('razon_social', 'nombre_corto', 'rfc', 'activo')
	search_fields = ('razon_social', 'rfc')
	list_filter = ('activo', 'fecha_actualizacion')
	readonly_fields = ('fecha_actualizacion',)
	
	fieldsets = (
		('Información General', {
			'fields': ('razon_social', 'nombre_corto', 'rfc', 'activo')
		}),
		('Domicilio', {
			'fields': ('domicilio', 'numero_exterior', 'colonia', 'codigo_postal', 'id_municipio')
		}),
		('Configuración SMTP', {
			'fields': ('smtp_host', 'smtp_puerto', 'smtp_usuario', 'smtp_contrasena', 'smtp_usar_tls', 'smtp_usar_ssl', 'correo_remitente'),
			'description': 'Configura los parámetros de tu servidor SMTP para enviar correos.'
		}),
		('Auditoría', {
			'fields': ('fecha_actualizacion',),
			'classes': ('collapse',)
		}),
	)


@admin.register(CatalogosDelegaciones)
class CatalogosDelegacionesAdmin(admin.ModelAdmin):
	list_display = ('nombre', 'municipio', 'telefono', 'responsable', 'activo')
	search_fields = ('nombre', 'telefono', 'correo', 'direccion')
	list_filter = ('activo', 'municipio', 'fecha_creacion')
	readonly_fields = ('fecha_creacion', 'fecha_modificacion')
	
	fieldsets = (
		('Información General', {
			'fields': ('nombre', 'municipio', 'activo')
		}),
		('Contacto', {
			'fields': ('telefono', 'correo', 'responsable')
		}),
		('Ubicación', {
			'fields': ('direccion', 'latitud', 'longitud', 'foto')
		}),
		('Horarios', {
			'fields': ('horario',)
		}),
		('Auditoría', {
			'fields': ('fecha_creacion', 'fecha_modificacion'),
			'classes': ('collapse',)
		}),
	)


@admin.register(PersonalDireccion)
class PersonalDireccionAdmin(admin.ModelAdmin):
	list_display = ('iddireccion', 'direccion', 'activo', 'fecha_captura', 'fecha_modificacion')
	list_filter = ('activo', 'fecha_captura', 'fecha_modificacion')
	search_fields = ('direccion', 'descripcion')
	readonly_fields = ('fecha_captura', 'fecha_modificacion', 'iddireccion')
	
	fieldsets = (
		('Información General', {
			'fields': ('iddireccion', 'direccion', 'descripcion', 'activo')
		}),
		('Auditoría', {
			'fields': ('usuario_captura', 'usuario_modificacion', 'fecha_captura', 'fecha_modificacion'),
			'classes': ('collapse',)
		}),
	)


@admin.register(PersonalDepartamento)
class PersonalDepartamentoAdmin(admin.ModelAdmin):
	list_display = ('iddepartamento', 'departamento', 'iddireccion', 'activo', 'fecha_captura')
	list_filter = ('activo', 'iddireccion', 'fecha_captura', 'fecha_modificacion')
	search_fields = ('departamento', 'descripcion', 'iddireccion__direccion')
	readonly_fields = ('fecha_captura', 'fecha_modificacion', 'iddepartamento')
	
	fieldsets = (
		('Información General', {
			'fields': ('iddepartamento', 'departamento', 'iddireccion', 'descripcion', 'activo')
		}),
		('Auditoría', {
			'fields': ('usuario_captura', 'usuario_modificacion', 'fecha_captura', 'fecha_modificacion'),
			'classes': ('collapse',)
		}),
	)


@admin.register(PersonalTipoDeContratacion)
class PersonalTipoDeContratacionAdmin(admin.ModelAdmin):
	list_display = ('idtipodecontratacion', 'nombre', 'activo', 'fecha_captura', 'fecha_modificacion')
	list_filter = ('activo', 'fecha_captura', 'fecha_modificacion')
	search_fields = ('nombre', 'descripcion')
	readonly_fields = ('fecha_captura', 'fecha_modificacion', 'idtipodecontratacion')
	
	fieldsets = (
		('Información General', {
			'fields': ('idtipodecontratacion', 'nombre', 'descripcion', 'activo')
		}),
		('Auditoría', {
			'fields': ('usuario_captura', 'usuario_modificacion', 'fecha_captura', 'fecha_modificacion'),
			'classes': ('collapse',)
		}),
	)


@admin.register(PersonalPuestos)
class PersonalPuestosAdmin(admin.ModelAdmin):
	list_display = ('idpuesto', 'nombre', 'activo', 'fecha_captura', 'fecha_modificacion')
	list_filter = ('activo', 'fecha_captura', 'fecha_modificacion')
	search_fields = ('nombre', 'descripcion')
	readonly_fields = ('fecha_captura', 'fecha_modificacion', 'idpuesto')
	
	fieldsets = (
		('Información General', {
			'fields': ('idpuesto', 'nombre', 'descripcion', 'activo')
		}),
		('Auditoría', {
			'fields': ('usuario_captura', 'usuario_modificacion', 'fecha_captura', 'fecha_modificacion'),
			'classes': ('collapse',)
		}),
	)


@admin.register(PersonalEmpleados)
class PersonalEmpleadosAdmin(admin.ModelAdmin):
	list_display = ('id_empleado', 'nombre_completo', 'usuario', 'email', 'idpuesto', 'iddepartamento', 'activo')
	list_filter = ('activo', 'idtipodecontratacion', 'iddepartamento', 'idpuesto', 'fecha_ingreso', 'fecha_creacion')
	search_fields = ('nombre_completo', 'usuario', 'email', 'curp', 'rfc', 'numero_empleado', 'apellido_paterno', 'apellido_materno', 'nombre')
	readonly_fields = ('fecha_creacion', 'fecha_modificacion', 'fecha_ultimo_login', 'id_empleado', 'nombre_completo')
	
	fieldsets = (
		('Autenticación', {
			'fields': ('id_empleado', 'usuario', 'email')
		}),
		('Nombre', {
			'fields': ('apellido_paterno', 'apellido_materno', 'nombre', 'nombre_completo'),
			'description': 'Los campos de apellido y nombre se combinan automáticamente para generar el nombre completo'
		}),
		('Información Personal', {
			'fields': ('fecha_nacimiento', 'sexo', 'telefono', 'domicilio', 'curp', 'rfc')
		}),
		('Información Laboral', {
			'fields': ('numero_empleado', 'iddepartamento', 'idpuesto', 'fecha_ingreso', 'idtipodecontratacion', 'salario')
		}),
		('Estado', {
			'fields': ('activo', 'is_active', 'is_staff', 'is_admin')
		}),
		('Seguridad', {
			'fields': ('recordar_dispositivo', 'token_dispositivo'),
			'classes': ('collapse',)
		}),
		('Auditoría', {
			'fields': ('fecha_creacion', 'fecha_modificacion', 'fecha_ultimo_login'),
			'classes': ('collapse',)
		}),
	)


@admin.register(TicketMantenimiento)
class TicketMantenimientoAdmin(admin.ModelAdmin):
	list_display = ('id_ticket_mantenimiento', 'asunto', 'solicitante', 'departamento_soporte', 'estado', 'prioridad', 'atendido_por', 'fecha_creacion')
	list_filter = ('estado', 'prioridad', 'tipo_equipo', 'departamento_soporte', 'solicita_formateo', 'equipo_retirado')
	search_fields = ('asunto', 'descripcion', 'equipo', 'numero_inventario', 'solicitante__nombre_completo')
	readonly_fields = ('fecha_creacion', 'fecha_actualizacion', 'folio')


@admin.register(TicketMantenimientoArchivo)
class TicketMantenimientoArchivoAdmin(admin.ModelAdmin):
	list_display = ('id_archivo', 'ticket', 'nombre_original', 'subido_por', 'fecha_subida')
	search_fields = ('nombre_original', 'ticket__asunto')


@admin.register(TicketMantenimientoSeguimiento)
class TicketMantenimientoSeguimientoAdmin(admin.ModelAdmin):
	list_display = ('id_seguimiento', 'ticket', 'tipo', 'autor', 'notificar_solicitante', 'fecha')
	list_filter = ('tipo', 'notificar_solicitante', 'fecha')
	search_fields = ('ticket__asunto', 'mensaje', 'autor__nombre_completo')


@admin.register(RecuperacionContrasena)
class RecuperacionContraseñaAdmin(admin.ModelAdmin):
	list_display = ('id', 'usuario', 'email', 'fecha_creacion', 'utilizado', 'esta_vigente')
	list_filter = ('utilizado', 'fecha_creacion', 'fecha_expiracion')
	search_fields = ('usuario__nombre_completo', 'email')
	readonly_fields = ('token', 'fecha_creacion', 'ip_origen')

@admin.register(ConfiguracionSistema)
class ConfiguracionSistemaAdmin(admin.ModelAdmin):
	list_display = ('nombre_corto', 'razon_social', 'rfc', 'email_desde', 'fecha_modificacion')
	search_fields = ('razon_social', 'nombre_corto', 'rfc')
	readonly_fields = ('fecha_creacion', 'fecha_modificacion')
	fieldsets = (
		('Información de la Empresa', {
			'fields': ('razon_social', 'nombre_corto', 'rfc', 'domicilio', 'telefono', 'sitio_web', 'logo')
		}),
		('Operación Interna', {
			'fields': ('departamento_soporte_mantenimiento', 'departamento_compras_requisiciones')
		}),
		('Configuración SMTP', {
			'fields': ('email_desde', 'smtp_host', 'smtp_port', 'smtp_usuario', 'smtp_contrasena', 'smtp_usar_tls'),
			'classes': ('collapse',)
		}),
		('Auditoría', {
			'fields': ('fecha_creacion', 'fecha_modificacion'),
			'classes': ('collapse',)
		}),
	)


@admin.register(UsuariosDelSistema)
class UsuariosDelSistemaAdmin(admin.ModelAdmin):
	list_display = ('usuario', 'correo', 'get_empleado', 'rol', 'activo', 'fecha_ultimo_login', 'fecha_creacion')
	list_filter = ('rol', 'activo', 'fecha_creacion')
	search_fields = ('usuario', 'correo', 'id_empleado__nombre_completo')
	readonly_fields = ('fecha_creacion', 'fecha_modificacion', 'fecha_ultimo_login')
	fieldsets = (
		('Usuario', {
			'fields': ('id_empleado', 'usuario', 'correo', 'contrasena')
		}),
		('Configuración', {
			'fields': ('rol', 'activo', 'requiere_cambio_contrasena')
		}),
		('Auditoría', {
			'fields': ('fecha_ultimo_login', 'fecha_creacion', 'fecha_modificacion', 'creado_por'),
			'classes': ('collapse',)
		}),
	)
	
	def get_empleado(self, obj):
		return obj.id_empleado.nombre_completo
	get_empleado.short_description = 'Empleado'


@admin.register(ColaCorreos)
class ColaCorreosAdmin(admin.ModelAdmin):
	list_display = ('email_destino', 'tipo_correo', 'estado_badge', 'numero_intentos', 'fecha_creacion', 'fecha_envio')
	search_fields = ('email_destino', 'asunto')
	list_filter = ('estado', 'tipo_correo', 'fecha_creacion', 'numero_intentos')
	readonly_fields = ('fecha_creacion', 'fecha_envio', 'numero_intentos', 'mensaje_error', 'asunto', 'contenido_texto', 'contenido_html')
	fieldsets = (
		('Destinatario', {
			'fields': ('email_destino', 'id_empleado')
		}),
		('Contenido', {
			'fields': ('tipo_correo', 'asunto', 'contenido_texto', 'contenido_html')
		}),
		('Estado', {
			'fields': ('estado', 'numero_intentos', 'mensaje_error')
		}),
		('Auditoría', {
			'fields': ('fecha_creacion', 'fecha_envio'),
			'classes': ('collapse',)
		}),
	)
	
	def estado_badge(self, obj):
		if obj.estado == 'enviado':
			return '<span style="color: green; font-weight: bold;">✓ Enviado</span>'
		elif obj.estado == 'pendiente':
			return '<span style="color: orange; font-weight: bold;">⏱ Pendiente</span>'
		elif obj.estado == 'error':
			return '<span style="color: red; font-weight: bold;">✗ Error</span>'
		return obj.estado
	estado_badge.short_description = 'Estado'
	estado_badge.allow_tags = True


@admin.register(RequisicionesClasificacion)
class RequisicionesClasificacionAdmin(admin.ModelAdmin):
	list_display = ('id_clasificacion', 'nombre', 'activo', 'fecha_modificacion')
	list_filter = ('activo',)
	search_fields = ('nombre', 'descripcion')


@admin.register(RequisicionesCatalogoArticulos)
class RequisicionesCatalogoArticulosAdmin(admin.ModelAdmin):
	list_display = ('id_articulo', 'nombre', 'clasificacion', 'unidad_medida', 'stock_actual', 'precio_referencia', 'activo')
	list_filter = ('activo', 'clasificacion', 'unidad_medida')
	search_fields = ('nombre', 'descripcion')


class RequisicionesSolicitudDetalleInline(admin.TabularInline):
	model = RequisicionesSolicitudDetalle
	extra = 0
	readonly_fields = ('subtotal', 'subtotal_entregado')


@admin.register(RequisicionesSolicitud)
class RequisicionesSolicitudAdmin(admin.ModelAdmin):
	list_display = ('id_requisicion', 'solicitante', 'departamento_solicitante', 'estatus', 'atendido_por', 'fecha_creacion', 'fecha_entrega')
	list_filter = ('estatus', 'departamento_solicitante', 'departamento_atencion')
	search_fields = ('solicitante__nombre_completo', 'departamento_solicitante__departamento', 'comentarios_compra')
	readonly_fields = ('folio', 'fecha_creacion', 'fecha_actualizacion', 'fecha_toma', 'fecha_para_entrega', 'fecha_entrega')
	inlines = [RequisicionesSolicitudDetalleInline]


@admin.register(RequisicionesDocumento)
class RequisicionesDocumentoAdmin(admin.ModelAdmin):
	list_display = ('id_documento', 'requisicion', 'tipo_documento', 'proveedor', 'subido_por', 'fecha_subida')
	list_filter = ('tipo_documento', 'fecha_subida')
	search_fields = ('nombre_original', 'proveedor', 'descripcion', 'requisicion__solicitante__nombre_completo')


@admin.register(RequisicionesSeguimiento)
class RequisicionesSeguimientoAdmin(admin.ModelAdmin):
	list_display = ('id_seguimiento', 'requisicion', 'tipo', 'autor', 'fecha')
	list_filter = ('tipo', 'fecha')
	search_fields = ('mensaje', 'requisicion__solicitante__nombre_completo')
