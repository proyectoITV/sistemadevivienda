from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.db import DatabaseError
from django.utils import timezone
from datetime import datetime, time
from decimal import Decimal, ROUND_HALF_UP

from .models import (
	SeguridadContactanos,
	PersonalEmpleados,
	PersonalTipoDeContratacion,
	PersonalPuestos,
	PersonalDireccion,
	PersonalDepartamento,
	ConfiguracionSistema,
	UsuariosDelSistema,
	TransparenciaGo,
	PatrimonioBienesDelInstituto,
	CatalogosMarcas,
	PatrimonioClasificacionSerap,
	PatrimonioClasificacionContraloria,
	PatrimonioProveedor,
	PatrimonioResguardo,
	PatrimonioEntregaDepartamento,
	FerInformacion,
	FerFondos,
	FerCatSubsidio,
	CatalogosSexo,
	CatalogosMunicipios,
	CatalogosAdministraciones,
	Vehiculos,
	VehiculosBitacora,
	VehiculoFoto,
	VehiculosProveedores,
	TicketMantenimiento,
	ViaticosPresupuestoDireccion,
	ViaticosSolicitud,
	ViaticosZonaTarifa,
	RequisicionesClasificacion,
	RequisicionesCatalogoArticulos,
	RequisicionesDocumento,
)


class SeguridadContactanosForm(forms.ModelForm):
	website = forms.CharField(required=False, widget=forms.HiddenInput)

	class Meta:
		model = SeguridadContactanos
		fields = [
			'nombre_completo',
			'email',
			'compania_organizacion',
			'telefono',
			'asunto',
			'mensaje',
		]
		widgets = {
			'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'nombre@correo.com'}),
			'compania_organizacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Empresa, dependencia o institución (opcional)'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto (opcional)'}),
			'asunto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto de tu mensaje'}),
			'mensaje': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe tu mensaje'}),
		}
		labels = {
			'nombre_completo': 'Nombre completo',
			'email': 'Correo electrónico',
			'compania_organizacion': 'Compañía / Organización',
			'telefono': 'Teléfono',
			'asunto': 'Asunto',
			'mensaje': 'Mensaje',
		}

	def clean_website(self):
		website = self.cleaned_data.get('website', '')
		if website:
			raise ValidationError('Solicitud inválida.')
		return website


class PersonalEmpleadosForm(forms.ModelForm):
	"""Formulario para crear y editar empleados con campos de Recursos Humanos"""
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		label='Contraseña',
		required=False,
		help_text='Déjalo en blanco si no deseas cambiar la contraseña. Solo se requiere si el empleado será usuario del sistema.'
	)
	
	# Campo adicional para seleccionar dirección (no está en el modelo)
	iddireccion = forms.ModelChoiceField(
		queryset=PersonalDireccion.objects.filter(activo=True),
		required=False,
		label='Dirección',
		widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_iddireccion'}),
		help_text='Selecciona una dirección para filtrar los departamentos'
	)
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		
		# Si estamos editando un empleado existente, pre-cargar la dirección
		if self.instance and self.instance.iddepartamento:
			self.fields['iddireccion'].initial = self.instance.iddepartamento.iddireccion_id
	
	class Meta:
		model = PersonalEmpleados
		fields = [
			# Identificación
			'usuario',
			'email',
			
			# Nombre dividido
			'apellido_paterno',
			'apellido_materno',
			'nombre',
			
			# Información personal
			'fotografia',
			'curp',
			'rfc',
			'fecha_nacimiento',
			'sexo',
			'telefono',
			'domicilio',
			
			# Información laboral
			'iddepartamento',
			'idpuesto',
			'numero_empleado',
			'fecha_ingreso',
			'idtipodecontratacion',
			'salario',
			'activo',
		]
		widgets = {
			# Identificación
			'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario (opcional)', 'required': False}),
			'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
			
			# Nombre dividido
			'apellido_paterno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido paterno'}),
			'apellido_materno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido materno (opcional)'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre(s)'}),
			
			# Información personal
			'fotografia': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'curp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XXXXXX000000HXXXXXX00', 'maxlength': '18'}),
			'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC (13 caracteres)', 'maxlength': '13'}),
			'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'sexo': forms.Select(attrs={'class': 'form-select'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'}),
			'domicilio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Domicilio completo'}),
			
			# Información laboral
			'iddepartamento': forms.Select(attrs={'class': 'form-select', 'id': 'id_iddepartamento'}),
			'idpuesto': forms.Select(attrs={'class': 'form-select'}),
			'numero_empleado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de empleado'}),
			'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'idtipodecontratacion': forms.Select(attrs={'class': 'form-select'}),
			'salario': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salario', 'step': '0.01'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'usuario': 'Nombre de Usuario',
			'email': 'Correo Electrónico',
			'apellido_paterno': 'Apellido Paterno',
			'apellido_materno': 'Apellido Materno',
			'nombre': 'Nombre(s)',
			'fotografia': 'Fotografía',
			'curp': 'CURP',
			'rfc': 'RFC',
			'fecha_nacimiento': 'Fecha de Nacimiento',
			'sexo': 'Sexo',
			'telefono': 'Teléfono',
			'domicilio': 'Domicilio',
			'iddepartamento': 'Departamento',
			'idpuesto': 'Puesto',
			'numero_empleado': 'Número de Empleado',
			'fecha_ingreso': 'Fecha de Ingreso',
			'idtipodecontratacion': 'Tipo de Contratación',
			'salario': 'Salario',
			'activo': 'Activo',
		}
	
	def save(self, commit=True):
		user = super().save(commit=False)
		password = self.cleaned_data.get('password')
		usuario = self.cleaned_data.get('usuario')
		
		# Almacenar temporalmente el password en texto plano para envío de email
		user._password_texto_plano = password if (password and usuario) else None
		
		# Solo establecer password si se proporciona y si el usuario está definido
		if password and usuario:
			user.set_password(password)
		elif not usuario:
			# Si no hay usuario, limpiar los campos de autenticación
			user.usuario = None
			user.password = ''
		
		if commit:
			user.save()
		return user


class PersonalDireccionForm(forms.ModelForm):
	class Meta:
		model = PersonalDireccion
		fields = ['direccion', 'descripcion', 'activo']
		widgets = {
			'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la dirección'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'direccion': 'Dirección',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}


class PersonalDepartamentoForm(forms.ModelForm):
	class Meta:
		model = PersonalDepartamento
		fields = ['departamento', 'iddireccion', 'descripcion', 'activo']
		widgets = {
			'departamento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del departamento'}),
			'iddireccion': forms.Select(attrs={'class': 'form-select'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'departamento': 'Departamento',
			'iddireccion': 'Dirección',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['iddireccion'].queryset = PersonalDireccion.objects.filter(activo=True).order_by('direccion')


class PersonalPuestosForm(forms.ModelForm):
	class Meta:
		model = PersonalPuestos
		fields = ['nombre', 'descripcion', 'activo']
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del puesto'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Puesto',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}


class PersonalTipoDeContratacionForm(forms.ModelForm):
	class Meta:
		model = PersonalTipoDeContratacion
		fields = ['nombre', 'descripcion', 'activo']
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del tipo de contratación'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Tipo de Contratación',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}

class ConfiguracionSistemaForm(forms.ModelForm):
	"""Formulario para configuración del sistema"""
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['departamento_soporte_mantenimiento'].queryset = PersonalDepartamento.objects.filter(activo=True).order_by('departamento')
		self.fields['departamento_compras_requisiciones'].queryset = PersonalDepartamento.objects.filter(activo=True).order_by('departamento')

	class Meta:
		model = ConfiguracionSistema
		fields = [
			'razon_social',
			'nombre_corto',
			'rfc',
			'domicilio',
			'smtp_host',
			'smtp_port',
			'smtp_usuario',
			'smtp_contrasena',
			'smtp_usar_tls',
			'email_desde',
			'telefono',
			'sitio_web',
			'logo',
			'tiempo_sesion_minutos',
			'duracion_intro_segundos',
			'departamento_soporte_mantenimiento',
			'departamento_compras_requisiciones',
		]
		widgets = {
			'razon_social': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Razón social'}),
			'nombre_corto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ITAVU'}),
			'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC (13 caracteres)', 'maxlength': '13'}),
			'domicilio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Domicilio completo'}),
			'smtp_host': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'smtp.gmail.com'}),
			'smtp_port': forms.NumberInput(attrs={'class': 'form-control', 'value': '587'}),
			'smtp_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario@gmail.com'}),
			'smtp_contrasena': forms.PasswordInput(attrs={'class': 'form-control'}),
			'smtp_usar_tls': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'email_desde': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'noreply@empresa.com'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
			'sitio_web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://ejemplo.com'}),
			'logo': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'tiempo_sesion_minutos': forms.NumberInput(attrs={'class': 'form-control', 'min': '5', 'max': '1440', 'step': '1'}),
			'duracion_intro_segundos': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '6', 'step': '1'}),
			'departamento_soporte_mantenimiento': forms.Select(attrs={'class': 'form-select'}),
			'departamento_compras_requisiciones': forms.Select(attrs={'class': 'form-select'}),
		}
		labels = {
			'razon_social': 'Razón Social',
			'nombre_corto': 'Nombre Corto',
			'rfc': 'RFC',
			'domicilio': 'Domicilio',
			'smtp_host': 'Servidor SMTP',
			'smtp_port': 'Puerto SMTP',
			'smtp_usuario': 'Usuario SMTP',
			'smtp_contrasena': 'Contraseña SMTP',
			'smtp_usar_tls': 'Usar TLS',
			'email_desde': 'Email Desde',
			'telefono': 'Teléfono',
			'sitio_web': 'Sitio Web',
			'logo': 'Logo',
			'tiempo_sesion_minutos': 'Tiempo de sesión (Inactividad) en minutos',
			'duracion_intro_segundos': 'Duración de Intro (Dashboard) en segundos',
			'departamento_soporte_mantenimiento': 'Departamento de Soporte para Mantenimiento',
			'departamento_compras_requisiciones': 'Departamento de Adquisiciones para Requisiciones y Compras',
		}


class RequisicionesCatalogoArticulosForm(forms.ModelForm):
	class Meta:
		model = RequisicionesCatalogoArticulos
		fields = [
			'nombre',
			'clasificacion',
			'descripcion',
			'unidad_medida',
			'stock_actual',
			'precio_referencia',
			'imagen',
			'activo',
		]
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del artículo'}),
			'clasificacion': forms.Select(attrs={'class': 'form-select'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción o detalles del artículo'}),
			'unidad_medida': forms.Select(attrs={'class': 'form-select'}),
			'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
			'precio_referencia': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '0.01'}),
			'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Artículo',
			'clasificacion': 'Clasificación',
			'descripcion': 'Descripción',
			'unidad_medida': 'Unidad de medida',
			'stock_actual': 'Stock disponible',
			'precio_referencia': 'Precio de referencia',
			'imagen': 'Imagen',
			'activo': 'Activo',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['clasificacion'].queryset = RequisicionesClasificacion.objects.filter(activo=True).order_by('nombre')


class RequisicionesDocumentoForm(forms.ModelForm):
	class Meta:
		model = RequisicionesDocumento
		fields = ['tipo_documento', 'detalle', 'proveedor', 'descripcion', 'archivo']
		widgets = {
			'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
			'detalle': forms.Select(attrs={'class': 'form-select'}),
			'proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Proveedor o razón social'}),
			'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción breve del documento'}),
			'archivo': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
		}
		labels = {
			'tipo_documento': 'Tipo de documento',
			'detalle': 'Artículo relacionado',
			'proveedor': 'Proveedor',
			'descripcion': 'Descripción',
			'archivo': 'Archivo PDF',
		}

	def __init__(self, *args, **kwargs):
		detalles_queryset = kwargs.pop('detalles_queryset', None)
		super().__init__(*args, **kwargs)
		if detalles_queryset is not None:
			self.fields['detalle'].queryset = detalles_queryset
			self.fields['detalle'].required = False

	def clean_archivo(self):
		archivo = self.cleaned_data.get('archivo')
		if archivo:
			if not archivo.name.lower().endswith('.pdf'):
				raise ValidationError('Solo se permiten archivos PDF para cotizaciones y facturas.')
			if archivo.size > 15 * 1024 * 1024:
				raise ValidationError('El archivo no debe superar 15 MB.')
		return archivo


class TicketMantenimientoCrearForm(forms.ModelForm):
	class Meta:
		model = TicketMantenimiento
		fields = [
			'asunto',
			'descripcion',
			'tipo_equipo',
			'equipo',
			'numero_inventario',
			'ubicacion',
			'prioridad',
			'solicita_formateo',
		]
		widgets = {
			'asunto': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '255', 'placeholder': 'Ej: Mi computadora ya no enciende'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe el problema, cuándo empezó y qué intentaste hacer'}),
			'tipo_equipo': forms.Select(attrs={'class': 'form-select'}),
			'equipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Equipo de recepción / Laptop Dell'}),
			'numero_inventario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Inventario o número de serie'}),
			'ubicacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Planta alta, oficina 4'}),
			'prioridad': forms.Select(attrs={'class': 'form-select'}),
			'solicita_formateo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'asunto': 'Asunto',
			'descripcion': 'Descripción del problema',
			'tipo_equipo': 'Tipo de equipo',
			'equipo': 'Equipo',
			'numero_inventario': 'Inventario / serie',
			'ubicacion': 'Ubicación',
			'prioridad': 'Prioridad',
			'solicita_formateo': 'Posible formateo requerido',
		}


class UsuariosDelSistemaForm(forms.ModelForm):
	"""Formulario para crear y editar usuarios del sistema"""
	
	contrasena_confirmacion = forms.CharField(
		widget=forms.PasswordInput(attrs={'class': 'form-control'}),
		label='Confirmar Contraseña',
		required=False,
		help_text='Repite la contraseña'
	)
	
	class Meta:
		model = UsuariosDelSistema
		fields = [
			'id_empleado',
			'usuario',
			'correo',
			'contrasena',
			'rol',
			'activo',
			'requiere_cambio_contrasena',
		]
		widgets = {
			'id_empleado': forms.Select(attrs={'class': 'form-select'}),
			'usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
			'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'usuario@empresa.com'}),
			'contrasena': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
			'rol': forms.Select(attrs={'class': 'form-select'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'requiere_cambio_contrasena': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'id_empleado': 'Empleado',
			'usuario': 'Nombre de Usuario',
			'correo': 'Correo Electrónico',
			'contrasena': 'Contraseña',
			'rol': 'Rol',
			'activo': 'Activo',
			'requiere_cambio_contrasena': 'Requiere Cambio de Contraseña',
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Filtrar solo empleados activos
		self.fields['id_empleado'].queryset = PersonalEmpleados.objects.filter(activo=True)
		self.fields['id_empleado'].label_from_instance = lambda obj: f"{obj.nombre_completo} ({obj.usuario})"
	
	def clean(self):
		cleaned_data = super().clean()
		contrasena = cleaned_data.get('contrasena')
		contrasena_confirmacion = cleaned_data.get('contrasena_confirmacion')
		
		# Si es creación (no hay instancia), validar que contraseña sea requerida
		if not self.instance.pk and not contrasena:
			raise ValidationError('La contraseña es requerida para nuevos usuarios.')
		
		# Si se proporciona contraseña, validar confirmación
		if contrasena and contrasena != contrasena_confirmacion:
			raise ValidationError('Las contraseñas no coinciden.')
		
		return cleaned_data
	
	def save(self, commit=True):
		user = super().save(commit=False)
		contrasena = self.cleaned_data.get('contrasena')
		
		# Si hay contraseña nueva, encriptarla
		if contrasena:
			user.contrasena = make_password(contrasena)
		
		if commit:
			user.save()
		
		return user


class FiltroUsuariosDelSistemaForm(forms.Form):
	"""Formulario para filtrar usuarios del sistema"""
	
	ROLES_CHOICES = [
		('', '-- Todos los roles --'),
	] + UsuariosDelSistema.ROLES_CHOICES
	
	ESTADOS_CHOICES = [
		('', '-- Todos los estados --'),
		('activo', 'Activos'),
		('inactivo', 'Inactivos'),
	]
	
	busqueda = forms.CharField(
		required=False,
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'placeholder': 'Buscar por usuario, correo o nombre de empleado'
		}),
		label='Búsqueda'
	)
	
	rol = forms.ChoiceField(
		required=False,
		choices=ROLES_CHOICES,
		widget=forms.Select(attrs={'class': 'form-select'}),
		label='Rol'
	)
	
	estado = forms.ChoiceField(
		required=False,
		choices=ESTADOS_CHOICES,
		widget=forms.Select(attrs={'class': 'form-select'}),
		label='Estado'
	)


class PatrimonioBienesDelInstitutoForm(forms.ModelForm):
	"""Formulario para crear y editar bienes del Instituto"""
	
	class Meta:
		model = PatrimonioBienesDelInstituto
		fields = [
			'numero_inventario_itavu',
			'numero_inventario_gobierno',
			'descripcion',
			'fotografia',
			'marca',
			'modelo',
			'serie',
			'tipo_equipo',
			'numinv_monitor',
			'numserie_monitor',
			'fecha_factura',
			'numero_factura',
			'archivo_factura',
			'costo_articulo',
			'proveedor',
			'clasificacion_serap',
			'clasificacion_contraloria',
			'idestatus',
			'baja_fecha',
			'baja_numero_oficio',
			'baja_oficio',
			'observaciones',
		]
		widgets = {
			'numero_inventario_itavu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de inventario ITAVU'}),
			'numero_inventario_gobierno': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de inventario Gobierno (opcional)'}),
			'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del bien'}),
			'fotografia': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'marca': forms.Select(attrs={'class': 'form-select select2-marca', 'data-placeholder': 'Buscar marca...'}),
			'modelo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Modelo (opcional)'}),
			'serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de serie (opcional)'}),
			'tipo_equipo': forms.Select(attrs={'class': 'form-select select2-tipo', 'data-placeholder': 'Selecciona tipo de equipo'}),
			'numinv_monitor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Num. Inv. Monitor (opcional)'}),
			'numserie_monitor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Núm. Serie Monitor (opcional)'}),
			'fecha_factura': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'numero_factura': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de factura (opcional)'}),
			'archivo_factura': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf', 'data-max-size': '10485760'}),
			'costo_articulo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Costo del artículo', 'step': '0.01'}),
			'proveedor': forms.Select(attrs={'class': 'form-select select2-proveedor', 'data-placeholder': 'Buscar proveedor...'}),
			'clasificacion_serap': forms.Select(attrs={'class': 'form-select select2-clasificacion', 'data-placeholder': 'Buscar clasificación...'}),
			'clasificacion_contraloria': forms.Select(attrs={'class': 'form-select select2-clasificacion', 'data-placeholder': 'Buscar clasificación...'}),
			'idestatus': forms.Select(attrs={'class': 'form-select select2-clasificacion', 'data-placeholder': 'Selecciona el estatus...'}),
			'baja_fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'baja_numero_oficio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de oficio (ej: OF-2024-001)'}),
			'baja_oficio': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf', 'data-max-size': '10485760'}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Observaciones (opcional)'}),
		}
		labels = {
			'numero_inventario_itavu': 'Número de Inventario ITAVU',
			'numero_inventario_gobierno': 'Número de Inventario Gobierno',
			'descripcion': 'Descripción',
			'fotografia': 'Fotografía',
			'marca': 'Marca',
			'modelo': 'Modelo',
			'serie': 'Número de Serie',
			'fecha_factura': 'Fecha de Factura',
			'numero_factura': 'Número de Factura',
			'archivo_factura': 'Archivo de Factura (PDF)',
			'costo_articulo': 'Costo del Artículo',
			'proveedor': 'Proveedor',
			'clasificacion_serap': 'Clasificación SERAP',
			'clasificacion_contraloria': 'Clasificación de Contraloría',
			'tipo_equipo': 'Tipo de Equipo',
			'numinv_monitor': 'Num. Inv. Monitor',
			'numserie_monitor': 'Num. Serie Monitor',
			'idestatus': 'Estatus del Registro',
			'baja_fecha': 'Fecha de Baja',
			'baja_numero_oficio': 'Número de Oficio',
			'baja_oficio': 'Oficio de Baja (PDF)',
			'observaciones': 'Observaciones',
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		try:
			marcas_qs = CatalogosMarcas.objects.filter(activo=True).order_by('nombre')
			proveedores_qs = PatrimonioProveedor.objects.filter(activo=True).order_by('nombre')
			serap_qs = PatrimonioClasificacionSerap.objects.filter(activo=True).order_by('nombre')
			contraloria_qs = PatrimonioClasificacionContraloria.objects.filter(activo=True).order_by('nombre')

			self.fields['marca'].queryset = marcas_qs
			self.fields['proveedor'].queryset = proveedores_qs
			self.fields['clasificacion_serap'].queryset = serap_qs
			self.fields['clasificacion_contraloria'].queryset = contraloria_qs

			# Opciones simples sin agrupamiento
			self.fields['marca'].choices = [('', '---------')] + list(marcas_qs.values_list('pk', 'nombre'))
			self.fields['proveedor'].choices = [('', '---------')] + list(proveedores_qs.values_list('pk', 'nombre'))
			self.fields['clasificacion_serap'].choices = [('', '---------')] + list(serap_qs.values_list('pk', 'nombre'))
			self.fields['clasificacion_contraloria'].choices = [('', '---------')] + list(contraloria_qs.values_list('pk', 'nombre'))
		except DatabaseError:
			self.fields['marca'].queryset = CatalogosMarcas.objects.none()
			self.fields['proveedor'].queryset = PatrimonioProveedor.objects.none()
			self.fields['clasificacion_serap'].queryset = PatrimonioClasificacionSerap.objects.none()
			self.fields['clasificacion_contraloria'].queryset = PatrimonioClasificacionContraloria.objects.none()
			self.fields['marca'].choices = [('', '---------')]
			self.fields['proveedor'].choices = [('', '---------')]
			self.fields['clasificacion_serap'].choices = [('', '---------')]
			self.fields['clasificacion_contraloria'].choices = [('', '---------')]


class CatalogosMarcasForm(forms.ModelForm):
	class Meta:
		model = CatalogosMarcas
		fields = ['nombre', 'descripcion', 'activo']
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la marca'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Marca',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}


class PatrimonioProveedorForm(forms.ModelForm):
	class Meta:
		model = PatrimonioProveedor
		fields = ['nombre', 'rfc', 'telefono', 'correo', 'domicilio', 'persona_contacto', 'descripcion', 'activo']
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
			'rfc': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RFC (opcional)', 'maxlength': '13'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
			'correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com (opcional)'}),
			'domicilio': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Domicilio (opcional)'}),
			'persona_contacto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Persona de contacto (opcional)'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Proveedor',
			'rfc': 'RFC',
			'telefono': 'Teléfono',
			'correo': 'Correo Electrónico',
			'domicilio': 'Domicilio',
			'persona_contacto': 'Persona de Contacto',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}


class PatrimonioClasificacionSerapForm(forms.ModelForm):
	class Meta:
		model = PatrimonioClasificacionSerap
		fields = ['nombre', 'descripcion', 'activo']
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la clasificación SERAP'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Clasificación SERAP',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}


class PatrimonioClasificacionContraloriaForm(forms.ModelForm):
	class Meta:
		model = PatrimonioClasificacionContraloria
		fields = ['nombre', 'descripcion', 'activo']
		widgets = {
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la clasificación de Contraloría'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción (opcional)'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'nombre': 'Clasificación de Contraloría',
			'descripcion': 'Descripción',
			'activo': 'Activo',
		}


class PatrimonioResguardoAsignacionForm(forms.ModelForm):
	"""Formulario para asignar un bien a un empleado"""
	class Meta:
		model = PatrimonioResguardo
		fields = ['bien', 'empleado', 'fecha_asignacion', 'numero_oficio', 'fecha_oficio', 'archivo_oficio', 'observaciones_asignacion']
		widgets = {
			'bien': forms.Select(attrs={'class': 'form-select select2-bien', 'required': True, 'data-placeholder': 'Buscar por No. Inventario ITAVU o descripción...'}),
			'empleado': forms.Select(attrs={'class': 'form-select select2-empleado', 'required': True, 'data-placeholder': 'Buscar por número, nombre o apellido...'}),
			'fecha_asignacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
			'numero_oficio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: OF-2026-001', 'maxlength': 100}),
			'fecha_oficio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'archivo_oficio': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf', 'data-max-size': '10485760'}),
			'observaciones_asignacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observaciones sobre la asignación o transferencia...'}),
		}
		labels = {
			'bien': 'Bien a Resguardar',
			'empleado': 'Empleado Responsable',
			'fecha_asignacion': 'Fecha de Asignación',
			'numero_oficio': 'Número de Oficio',
			'fecha_oficio': 'Fecha del Oficio',
			'archivo_oficio': 'Archivo del Oficio (PDF)',
			'observaciones_asignacion': 'Observaciones',
		}
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Mostrar TODOS los bienes activos con formato mejorado
		self.fields['bien'].queryset = PatrimonioBienesDelInstituto.objects.filter(activo=True).order_by('numero_inventario_itavu')
		# Personalizar cómo se muestran los bienes
		self.fields['bien'].label_from_instance = lambda obj: f"{obj.numero_inventario_itavu} - {obj.descripcion}"
		
		# Filtrar solo empleados activos
		self.fields['empleado'].queryset = PersonalEmpleados.objects.filter(activo=True).order_by('numero_empleado', 'nombre', 'apellido_paterno')
		# Personalizar cómo se muestran los empleados
		self.fields['empleado'].label_from_instance = lambda obj: f"{obj.numero_empleado} - {obj.nombre} {obj.apellido_paterno} {obj.apellido_materno}".strip()
	
	def clean_archivo_oficio(self):
		archivo = self.cleaned_data.get('archivo_oficio')
		if archivo:
			# Validar que sea un PDF
			if not archivo.name.lower().endswith('.pdf'):
				raise ValidationError('El archivo debe ser un PDF.')
			# Validar tamaño (máximo 10 MB)
			if archivo.size > 10485760:  # 10 MB
				raise ValidationError('El archivo no debe superar 10 MB.')
		return archivo


class PatrimonioResguardoDevolucionForm(forms.ModelForm):
	"""Formulario para registrar la devolución de un bien"""
	class Meta:
		model = PatrimonioResguardo
		fields = ['fecha_devolucion', 'observaciones_devolucion']
		widgets = {
			'fecha_devolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
			'observaciones_devolucion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observaciones sobre la devolución...'}),
		}
		labels = {
			'fecha_devolucion': 'Fecha de Devolución',
			'observaciones_devolucion': 'Observaciones de Devolución',
		}


class PatrimonioEntregaDepartamentoForm(forms.ModelForm):
	"""Formulario para entrega-recepción total de bienes por cambio de responsable de departamento"""

	class Meta:
		model = PatrimonioEntregaDepartamento
		fields = ['empleado_saliente', 'empleado_entrante', 'fecha_entrega', 'observaciones']
		widgets = {
			'empleado_saliente': forms.Select(attrs={'class': 'form-select', 'required': True}),
			'empleado_entrante': forms.Select(attrs={'class': 'form-select', 'required': True}),
			'fecha_entrega': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': True}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observaciones sobre la entrega-recepción (opcional)...'}),
		}
		labels = {
			'empleado_saliente': 'Empleado que Entrega',
			'empleado_entrante': 'Empleado que Recibe',
			'fecha_entrega': 'Fecha de Entrega-Recepción',
			'observaciones': 'Observaciones',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		empleados_qs = PersonalEmpleados.objects.filter(activo=True, iddepartamento__isnull=False).select_related('iddepartamento').order_by('numero_empleado', 'nombre', 'apellido_paterno')
		self.fields['empleado_saliente'].queryset = empleados_qs
		self.fields['empleado_entrante'].queryset = empleados_qs

		self.fields['empleado_saliente'].label_from_instance = lambda obj: f"{obj.numero_empleado} - {obj.nombre} {obj.apellido_paterno} ({obj.iddepartamento.departamento})"
		self.fields['empleado_entrante'].label_from_instance = lambda obj: f"{obj.numero_empleado} - {obj.nombre} {obj.apellido_paterno} ({obj.iddepartamento.departamento})"

	def clean(self):
		cleaned_data = super().clean()
		empleado_saliente = cleaned_data.get('empleado_saliente')
		empleado_entrante = cleaned_data.get('empleado_entrante')

		if not empleado_saliente or not empleado_entrante:
			return cleaned_data

		if empleado_saliente.idempleado == empleado_entrante.idempleado:
			raise ValidationError('El empleado que entrega y el que recibe deben ser diferentes.')

		if not empleado_saliente.iddepartamento or not empleado_entrante.iddepartamento:
			raise ValidationError('Ambos empleados deben tener departamento asignado.')

		if empleado_saliente.iddepartamento_id != empleado_entrante.iddepartamento_id:
			raise ValidationError('La entrega-recepción solo se permite entre empleados del mismo departamento.')

		resguardos_activos = PatrimonioResguardo.objects.filter(empleado=empleado_saliente, activo=True).count()
		if resguardos_activos == 0:
			raise ValidationError('El empleado que entrega no tiene bienes activos para transferir.')

		return cleaned_data


# ==================== FORMULARIOS DE FER ====================

class FerInformacionForm(forms.ModelForm):
	"""Formulario para crear/editar información del FER"""
	class Meta:
		model = FerInformacion
		fields = [
			'nfer_id', 'contrato', 'nombre', 'curp',
			'descripcion', 'cantidad', 'nfer_concepto', 'fechanacimiento',
			'domicilio', 'telefono', 'celular', 'id_municipio',
			'id_sexo', 'parrafo_opcional', 'archivo_sustento'
		]
		widgets = {
			'nfer_id': forms.NumberInput(attrs={'class': 'form-control', 'type': 'number', 'placeholder': 'ID del beneficiario', 'readonly': 'readonly'}),
			'contrato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de contrato'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo del beneficiario', 'style': 'text-transform: uppercase;'}),
			'curp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CURP del beneficiario', 'style': 'text-transform: uppercase;'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del concepto'}),
			'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Cantidad en pesos'}),
			'nfer_concepto': forms.Select(attrs={'class': 'form-control form-select'}),
			'fechanacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'domicilio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Domicilio del beneficiario'}),
			'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono de contacto'}),
			'celular': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Celular de contacto'}),
			'id_municipio': forms.Select(attrs={'class': 'form-control form-select'}),
			'id_sexo': forms.Select(attrs={'class': 'form-control form-select'}),
			'parrafo_opcional': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Párrafo adicional (opcional)'}),
			'archivo_sustento': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx,.jpg,.jpeg,.png'}),
		}
		labels = {
			'nfer_id': 'ID del Beneficiario',
			'contrato': 'Número de Contrato',
			'nombre': 'Nombre del Beneficiario',
			'curp': 'CURP',
			'descripcion': 'Descripción',
			'cantidad': 'Cantidad',
			'nfer_concepto': 'Concepto de Subsidio',
			'fechanacimiento': 'Fecha de Nacimiento',
			'domicilio': 'Domicilio',
			'telefono': 'Teléfono',
			'celular': 'Celular',
			'id_municipio': 'Municipio',
			'id_sexo': 'Sexo',
			'parrafo_opcional': 'Párrafo Opcional',
			'archivo_sustento': 'Archivo de Sustento',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# Filtrar municipios activos
		self.fields['id_municipio'].queryset = CatalogosMunicipios.objects.filter().select_related('entidad')
		# Filtrar sexos activos
		self.fields['id_sexo'].queryset = CatalogosSexo.objects.filter(activo=True)
		# Filtrar conceptos de subsidio activos
		self.fields['nfer_concepto'].queryset = FerCatSubsidio.objects.filter(activo=True)
		# Establecer valores por defecto cuando se crea un nuevo registro
		if not self.instance.pk:
			import datetime
			# Calcular nfer_id dentro de la administración actual
			try:
				administracion_actual = CatalogosAdministraciones.objects.filter(
					fechainicio__lte=datetime.date.today(),
					fechatermino__gte=datetime.date.today()
				).first()
				if administracion_actual:
					# Calcular max local y evitar colisión global
					last_nfer = FerInformacion.objects.filter(
						autorizo_fecha__gte=administracion_actual.fechainicio,
						autorizo_fecha__lte=administracion_actual.fechatermino
					).order_by('-nfer_id').first()
					candidate = (last_nfer.nfer_id + 1) if last_nfer else 1
					while FerInformacion.objects.filter(nfer_id=candidate).exists():
						candidate += 1
					self.fields['nfer_id'].initial = candidate
				else:
					last_global = FerInformacion.objects.order_by('-nfer_id').first()
					self.fields['nfer_id'].initial = (last_global.nfer_id + 1) if last_global else 1
			except Exception:
				self.fields['nfer_id'].initial = 1

	def clean_nombre(self):
		nombre = self.cleaned_data.get('nombre')
		if nombre:
			return nombre.upper()
		return nombre

	def clean_curp(self):
		curp = self.cleaned_data.get('curp')
		if curp and len(curp) != 18:
			raise ValidationError('El CURP debe tener 18 caracteres.')
		return curp.upper() if curp else curp

	def clean_nfer_id(self):
		nfer_id = self.cleaned_data.get('nfer_id')
		if nfer_id is None:
			return nfer_id
		qs = FerInformacion.objects.filter(nfer_id=nfer_id)
		if self.instance.pk:
			qs = qs.exclude(pk=self.instance.pk)
		if qs.exists():
			raise ValidationError('Ya existe un registro con este ID de beneficiario.')
		return nfer_id

	def clean_archivo_sustento(self):
		archivo = self.cleaned_data.get('archivo_sustento')
		if archivo and hasattr(archivo, 'size'):
			# Validar tamaño (máximo 5 MB)
			if archivo.size > 5242880:  # 5 MB
				raise ValidationError('El archivo no debe superar 5 MB.')
			# Validar extensión
			extensiones_permitidas = ['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx']
			ext = archivo.name.split('.')[-1].lower()
			if ext not in extensiones_permitidas:
				raise ValidationError('El archivo debe ser PDF, imagen o documento Word.')
		return archivo
class TransparenciaArchivoUploadForm(forms.Form):
	archivo_pdf = forms.FileField(
		label='Archivo PDF',
		widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf', 'required': True})
	)
	nombre = forms.CharField(
		label='Nombre',
		max_length=255,
		widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre para publicar el archivo', 'required': True})
	)
	comentarios = forms.CharField(
		label='Comentarios',
		required=False,
		widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observaciones adicionales (opcional)'})
	)

	def clean_archivo_pdf(self):
		archivo = self.cleaned_data.get('archivo_pdf')
		if not archivo:
			raise ValidationError('Debes seleccionar un archivo PDF.')

		nombre_archivo = archivo.name.lower()
		if not nombre_archivo.endswith('.pdf'):
			raise ValidationError('Solo se permiten archivos con extension .pdf.')

		# Limite de 20 MB para prevenir cargas excesivas
		if archivo.size > 20 * 1024 * 1024:
			raise ValidationError('El archivo no debe superar 20 MB.')

		return archivo


class ViaticosPresupuestoDireccionForm(forms.ModelForm):
	class Meta:
		model = ViaticosPresupuestoDireccion
		fields = ['iddireccion', 'ejercicio', 'monto_asignado', 'activo', 'observaciones']
		widgets = {
			'iddireccion': forms.Select(attrs={'class': 'form-select'}),
			'ejercicio': forms.NumberInput(attrs={'class': 'form-control', 'min': '2024'}),
			'monto_asignado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notas del presupuesto (opcional)'}),
		}
		labels = {
			'iddireccion': 'Direccion',
			'ejercicio': 'Ejercicio',
			'monto_asignado': 'Monto asignado',
			'activo': 'Activo',
			'observaciones': 'Observaciones',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['iddireccion'].queryset = PersonalDireccion.objects.filter(activo=True).order_by('direccion')


class ViaticosZonaTarifaForm(forms.ModelForm):
	class Meta:
		model = ViaticosZonaTarifa
		fields = ['clave', 'nombre', 'hospedaje_noche', 'alimentacion_diaria', 'combustible_km', 'activo']
		widgets = {
			'clave': forms.Select(attrs={'class': 'form-select'}),
			'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre visible de la zona'}),
			'hospedaje_noche': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
			'alimentacion_diaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
			'combustible_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001', 'min': '0'}),
			'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
		}
		labels = {
			'clave': 'Zona',
			'nombre': 'Nombre',
			'hospedaje_noche': 'Hospedaje por noche',
			'alimentacion_diaria': 'Alimentacion diaria',
			'combustible_km': 'Combustible por km',
			'activo': 'Activo',
		}


class ViaticosSolicitudForm(forms.ModelForm):
	class Meta:
		model = ViaticosSolicitud
		fields = [
			'empleado',
			'zona',
			'motivo_comision',
			'origen',
			'destino',
			'origen_latitud',
			'origen_longitud',
			'destino_latitud',
			'destino_longitud',
			'distancia_km',
			'viaje_redondo',
			'dias',
			'transporte',
			'pasajes_estimados',
			'taxis_estimados',
			'observaciones',
		]
		widgets = {
			'empleado': forms.Select(attrs={'class': 'form-select select2-enhanced', 'data-placeholder': 'Buscar por numero, nombre o apellidos...'}),
			'zona': forms.Select(attrs={'class': 'form-select'}),
			'motivo_comision': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Objetivo, reunion, supervision o actividad a realizar'}),
			'origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ciudad Victoria, Tamaulipas'}),
			'destino': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Reynosa, Tamaulipas'}),
			'origen_latitud': forms.HiddenInput(),
			'origen_longitud': forms.HiddenInput(),
			'destino_latitud': forms.HiddenInput(),
			'destino_longitud': forms.HiddenInput(),
			'distancia_km': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'readonly': 'readonly'}),
			'viaje_redondo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
			'dias': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
			'transporte': forms.Select(attrs={'class': 'form-select'}),
			'pasajes_estimados': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
			'taxis_estimados': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
			'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Restricciones, agenda, numero de oficio o datos complementarios'}),
		}
		labels = {
			'empleado': 'Empleado comisionado',
			'zona': 'Zona tarifaria',
			'motivo_comision': 'Motivo de la comision',
			'origen': 'Origen',
			'destino': 'Destino',
			'distancia_km': 'Distancia referencial (km)',
			'viaje_redondo': 'Considerar viaje redondo',
			'dias': 'Dias de comision',
			'transporte': 'Medio de transporte principal',
			'pasajes_estimados': 'Pasajes estimados',
			'taxis_estimados': 'Taxis estimados',
			'observaciones': 'Observaciones',
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['empleado'].queryset = (
			PersonalEmpleados.objects
			.filter(activo=True, iddepartamento__isnull=False, iddepartamento__iddireccion__isnull=False)
			.select_related('iddepartamento', 'iddepartamento__iddireccion')
			.order_by('numero_empleado', 'nombre_completo')
		)
		self.fields['empleado'].label_from_instance = self._label_empleado
		self.fields['zona'].queryset = ViaticosZonaTarifa.objects.filter(activo=True).order_by('nombre')

	def _label_empleado(self, empleado):
		numero = empleado.numero_empleado or f"ID {empleado.id_empleado}"
		departamento = empleado.iddepartamento.departamento if empleado.iddepartamento else 'Sin departamento'
		return f"{numero} | {empleado.nombre_completo} | {departamento}"

	def clean(self):
		cleaned_data = super().clean()
		empleado = cleaned_data.get('empleado')

		if not empleado:
			return cleaned_data

		departamento = empleado.iddepartamento
		if departamento is None or departamento.iddireccion is None:
			raise ValidationError('El empleado seleccionado no tiene direccion configurada.')

		ejercicio_actual = timezone.localdate().year
		presupuesto = (
			ViaticosPresupuestoDireccion.objects
			.filter(iddireccion=departamento.iddireccion, ejercicio=ejercicio_actual, activo=True)
			.order_by('-fecha_modificacion')
			.first()
		)
		if presupuesto is None:
			raise ValidationError(
				f'No existe presupuesto activo de viaticos para {departamento.iddireccion.direccion} en {ejercicio_actual}.'
			)

		self.instance.empleado = empleado
		self.instance.direccion = departamento.iddireccion
		self.instance.presupuesto = presupuesto
		return cleaned_data


class VehiculosForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for nombre_campo, campo in self.fields.items():
			if isinstance(campo.widget, forms.Select):
				css = campo.widget.attrs.get('class', '')
				campo.widget.attrs['class'] = f"{css} select2-enhanced".strip()

		if 'idareaadscripcion' in self.fields:
			self.fields['idareaadscripcion'].queryset = PersonalDepartamento.objects.filter(activo=True).order_by('departamento')

		if 'idresguradante' in self.fields:
			self.fields['idresguradante'].queryset = PersonalEmpleados.objects.filter(activo=True).order_by('nombre_completo')
			self.fields['idresguradante'].label_from_instance = lambda obj: obj.nombre_completo

	class Meta:
		model = Vehiculos
		fields = [
			'num_economico',
			'clave_marca',
			'tipo',
			'clave_color',
			'modelo',
			'placas',
			'serie',
			'idestatus',
			'idareaadscripcion',
			'idresguradante',
			'comentario',
			'cilindros',
			'idpropietario',
		]
		widgets = {
			'num_economico': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numero economico'}),
			'clave_marca': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Selecciona una marca'}),
			'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de vehiculo'}),
			'clave_color': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Selecciona un color'}),
			'modelo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Modelo (anio)'}),
			'placas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placas'}),
			'serie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Serie'}),
			'idestatus': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Selecciona estatus'}),
			'idareaadscripcion': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Selecciona area de adscripcion'}),
			'idresguradante': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Selecciona resguardante'}),
			'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Comentario (opcional)'}),
			'cilindros': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Numero de cilindros'}),
			'idpropietario': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Selecciona propietario'}),
		}
		labels = {
			'clave_color': 'Color',
			'clave_marca': 'Marca',
			'idestatus': 'Estatus',
			'idareaadscripcion': 'Area de Adscripcion',
			'idresguradante': 'Resguardante',
		}


class VehiculosBitacoraForm(forms.ModelForm):
	fecha_solicitud = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
	fecha_ejecucion = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

	def __init__(self, *args, **kwargs):
		vehiculo = kwargs.pop('vehiculo', None)
		super().__init__(*args, **kwargs)
		self.fields['num_economico'].queryset = self.fields['num_economico'].queryset.filter(idestatus_id=0).order_by('num_economico')
		if vehiculo is not None:
			self.fields['num_economico'].initial = vehiculo.pk
			self.fields['num_economico'].queryset = self.fields['num_economico'].queryset.filter(pk=vehiculo.pk)
		self.fields['num_economico'].widget = forms.HiddenInput()

		for nombre_campo, campo in self.fields.items():
			if isinstance(campo.widget, forms.Select):
				css = campo.widget.attrs.get('class', '')
				campo.widget.attrs['class'] = f"{css} select2-enhanced".strip()

	class Meta:
		model = VehiculosBitacora
		fields = [
			'num_economico',
			'fecha_solicitud',
			'fecha_ejecucion',
			'km_prog',
			'km_real',
			'num_solicitud',
			'num_factura',
			'costo_mano_obra',
			'costo_refaccion',
			'importe_factura',
			'clave_tipo_mant',
			'clave_proveedor',
			'descripcion',
			'archivo_factura',
		]
		widgets = {
			'num_economico': forms.HiddenInput(),
			'fecha_solicitud': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'fecha_ejecucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'clave_tipo_mant': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Buscar tipo de servicio...'}),
			'km_prog': forms.NumberInput(attrs={'class': 'form-control'}),
			'km_real': forms.NumberInput(attrs={'class': 'form-control'}),
			'num_solicitud': forms.NumberInput(attrs={'class': 'form-control'}),
			'num_factura': forms.TextInput(attrs={'class': 'form-control'}),
			'clave_proveedor': forms.Select(attrs={'class': 'form-select', 'data-placeholder': 'Buscar proveedor...'}),
			'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
			'costo_mano_obra': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
			'costo_refaccion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
			'importe_factura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
			'archivo_factura': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'}),
		}
		labels = {
			'fecha_solicitud': 'Fecha de Solicitud',
			'fecha_ejecucion': 'Fecha de ejecucion',
			'km_prog': 'Km_prog',
			'km_real': 'Km_real',
			'num_solicitud': 'Num. de solicitud',
			'num_factura': 'Num. de Factura',
			'costo_mano_obra': 'Costo de mano de obra',
			'costo_refaccion': 'Costo de refaccion',
			'importe_factura': 'Importe factura',
			'clave_tipo_mant': 'Tipo de Servicio',
			'clave_proveedor': 'Proveedor',
			'descripcion': 'Descripcion',
			'archivo_factura': 'Archivo de Factura',
		}

	def clean_fecha_solicitud(self):
		fecha = self.cleaned_data.get('fecha_solicitud')
		if fecha and not isinstance(fecha, datetime):
			return datetime.combine(fecha, time.min)
		return fecha

	def clean_fecha_ejecucion(self):
		fecha = self.cleaned_data.get('fecha_ejecucion')
		if fecha and not isinstance(fecha, datetime):
			return datetime.combine(fecha, time.min)
		return fecha

	def _round_money(self, value):
		if value is None:
			return value
		return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

	def clean_costo_mano_obra(self):
		return self._round_money(self.cleaned_data.get('costo_mano_obra'))

	def clean_costo_refaccion(self):
		return self._round_money(self.cleaned_data.get('costo_refaccion'))

	def clean_importe_factura(self):
		return self._round_money(self.cleaned_data.get('importe_factura'))


class VehiculoFotoForm(forms.ModelForm):
	class Meta:
		model = VehiculoFoto
		fields = ['imagen', 'descripcion']
		widgets = {
			'imagen': forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
			'descripcion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripcion (opcional)'}),
		}


class VehiculosProveedorForm(forms.ModelForm):
	class Meta:
		model = VehiculosProveedores
		fields = ['nombre_proveedor']
		widgets = {
			'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
		}
		labels = {
			'nombre_proveedor': 'Proveedor',
		}
