# -*- coding: utf-8 -*-
"""
Vistas para el módulo de Fondo Económico de Reserva (FER)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, FileResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime
import json

from .models import FerInformacion, FerFondos, FerCatSubsidio, CatalogosSexo
from .forms import FerInformacionForm


@login_required
@require_http_methods(["GET"])
def fer_asignacion_listado(request):
	"""Vista de listado de asignaciones de FER (Asignación de Recurso)"""
	try:
		# Obtener el año fiscal elegido o el año actual
		ejercicio = request.GET.get('ejercicio', datetime.now().year)
		
		# Obtener registros del año fiscal con estado activo
		registros = FerInformacion.objects.filter(
			ejercicio=int(ejercicio),
			estado=0  # Solo activos
		).select_related('nfer_concepto', 'idmunicipio', 'sexo').order_by('-numcertificado')
		
		# Obtener fondo del año fiscal
		fondo_ejercicio = FerFondos.objects.filter(ejercicio=int(ejercicio)).first()
		
		# Calcular totales
		total_asignado = registros.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
		fondo_disponible = 0
		if fondo_ejercicio:
			fondo_disponible = fondo_ejercicio.fondo - total_asignado
		
		# Obtener años disponibles
		años_disponibles = FerFondos.objects.order_by('-ejercicio').values_list('ejercicio', flat=True).distinct()
		
		context = {
			'registros': registros,
			'ejercicio_actual': int(ejercicio),
			'años_disponibles': años_disponibles,
			'total_asignado': float(total_asignado),
			'fondo_ejercicio': fondo_ejercicio.fondo if fondo_ejercicio else 0,
			'fondo_disponible': float(fondo_disponible),
		}
		
		return render(request, 'desarrollo/fer/asignacion_listado.html', context)
	except Exception as e:
		messages.error(request, f'Error al cargar los registros: {str(e)}')
		return render(request, 'desarrollo/fer/asignacion_listado.html', {'registros': []})


@login_required
@require_http_methods(["GET", "POST"])
def fer_informacion_crear(request):
	"""Vista para crear nuevo registro de FER"""
	if request.method == 'POST':
		form = FerInformacionForm(request.POST, request.FILES)
		if form.is_valid():
			fer_info = form.save(commit=False)
			fer_info.idempmodifica = getattr(request.user, 'usuario', request.user.username)
			fer_info.fechaultimamod = timezone.now().date()
			fer_info.save()
			messages.success(request, f'Registro del beneficiario "{fer_info.nombre}" creado exitosamente.')
			return redirect('fer_asignacion_listado')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{field}: {error}')
	else:
		form = FerInformacionForm()
	
	context = {
		'form': form,
		'titulo': 'Nuevo Registro FER',
	}
	return render(request, 'desarrollo/fer/formulario_fer.html', context)


@login_required
@require_http_methods(["GET", "POST"])
def fer_informacion_editar(request, nfer_id):
	"""Vista para editar registro de FER"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id)
	
	if request.method == 'POST':
		form = FerInformacionForm(request.POST, request.FILES, instance=fer_info)
		if form.is_valid():
			fer_info = form.save(commit=False)
			fer_info.idempmodifica = getattr(request.user, 'usuario', request.user.username)
			fer_info.fechaultimamod = timezone.now().date()
			fer_info.save()
			messages.success(request, f'Registro del beneficiario "{fer_info.nombre}" actualizado exitosamente.')
			return redirect('fer_asignacion_listado')
		else:
			for field, errors in form.errors.items():
				for error in errors:
					messages.error(request, f'{field}: {error}')
	else:
		form = FerInformacionForm(instance=fer_info)
	
	context = {
		'form': form,
		'titulo': f'Editar Registro - {fer_info.nombre}',
		'fer_info': fer_info,
	}
	return render(request, 'desarrollo/fer/formulario_fer.html', context)


@login_required
@require_http_methods(["GET"])
def fer_informacion_detalle(request, nfer_id):
	"""Vista para ver detalle completo del registro FER"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id)
	
	context = {
		'fer_info': fer_info,
	}
	return render(request, 'desarrollo/fer/detalle_fer.html', context)


@login_required
@require_http_methods(["POST"])
def fer_informacion_inactivar(request, nfer_id):
	"""Vista para marcar registro FER como inactivo"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id)
	
	fer_info.estado = 1  # Marcar como inactivo
	fer_info.idempmodifica = getattr(request.user, 'usuario', request.user.username)
	fer_info.fechaultimamod = timezone.now().date()
	fer_info.save()
	
	messages.success(request, f'El registro del beneficiario "{fer_info.nombre}" ha sido marcado como inactivo.')
	return redirect('fer_asignacion_listado')


@login_required
@require_http_methods(["GET"])
def fer_certificado_generar(request, nfer_id):
	"""Vista para generar PDF del certificado de subsidio"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id)
	
	try:
		from reportlab.lib.pagesizes import letter
		from reportlab.lib import colors
		from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
		from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
		from reportlab.lib.units import inch
		from datetime import datetime
		from io import BytesIO
		
		# Crear buffer para PDF
		buffer = BytesIO()
		
		# Crear documento
		doc = SimpleDocTemplate(
			buffer,
			pagesize=letter,
			rightMargin=0.5*inch,
			leftMargin=0.5*inch,
			topMargin=0.5*inch,
			bottomMargin=0.5*inch,
		)
		
		# Estilos
		styles = getSampleStyleSheet()
		style_title = ParagraphStyle(
			'CustomTitle',
			parent=styles['Heading1'],
			fontSize=16,
			textColor=colors.HexColor('#8B0000'),
			spaceAfter=20,
			alignment=1,  # Center
		)
		
		style_normal = ParagraphStyle(
			'CustomNormal',
			parent=styles['Normal'],
			fontSize=10,
			leading=14,
		)
		
		# Contenido del documento
		content = []
		
		# Encabezado (Logo y título)
		content.append(Paragraph(
			'<b>CERTIFICADO DE SUBSIDIO ESTATAL</b>',
			style_title
		))
		
		content.append(Paragraph(
			f'<b>Fondo Económico de Reserva - Ejercicio {fer_info.ejercicio}</b>',
			styles['Heading3']
		))
		
		content.append(Spacer(1, 0.3*inch))
		
		# Información del beneficiario
		info_text = f"""
		<b>Beneficiario:</b> {fer_info.nombre}<br/>
		<b>CURP:</b> {fer_info.curp}<br/>
		<b>Fecha de Nacimiento:</b> {fer_info.nacimiento.strftime('%d/%m/%Y')}<br/>
		<b>Sexo:</b> {fer_info.sexo.sexo}<br/>
		<b>Domicilio:</b> {fer_info.domicilio}<br/>
		<b>Municipio:</b> {fer_info.idmunicipio.nombre}<br/>
		<b>Teléfono:</b> {fer_info.telefono}<br/>
		<b>Celular:</b> {fer_info.celular}<br/>
		"""
		content.append(Paragraph(info_text, style_normal))
		
		content.append(Spacer(1, 0.2*inch))
		
		# Información del subsidio
		subsidio_text = f"""
		<b>Número de Certificado:</b> {fer_info.numcertificado}<br/>
		<b>Número de Contrato:</b> {fer_info.contrato}<br/>
		<b>Concepto:</b> {fer_info.nfer_concepto.fer_descripcion}<br/>
		<b>Cantidad Otorgada:</b> ${fer_info.cantidad:,.2f}<br/>
		<b>Descripción:</b> {fer_info.descripcion}<br/>
		"""
		content.append(Paragraph(subsidio_text, style_normal))
		
		content.append(Spacer(1, 0.2*inch))
		
		# Información de autorización
		autorizacion_text = f"""
		<b>Autorizado por:</b> {fer_info.autorizo}<br/>
		<b>Fecha de Autorización:</b> {fer_info.autorizo_fecha.strftime('%d/%m/%Y')}<br/>
		<b>Hora:</b> {fer_info.autorizo_hora.strftime('%H:%M')}<br/>
		"""
		content.append(Paragraph(autorizacion_text, style_normal))
		
		if fer_info.parrafo_opcional:
			content.append(Spacer(1, 0.2*inch))
			content.append(Paragraph(fer_info.parrafo_opcional, style_normal))
		
		content.append(Spacer(1, 0.5*inch))
		
		# Pie de página
		pie_text = f"""
		<b>Generado el:</b> {timezone.now().strftime('%d/%m/%Y a las %H:%M:%S')}<br/>
		<b>Documento:</b> FER_{fer_info.ejercicio}_{fer_info.numcertificado:05d}
		"""
		content.append(Paragraph(pie_text, styles['Normal']))
		
		# Construir PDF
		doc.build(content)
		
		# Retornar PDF
		buffer.seek(0)
		return FileResponse(
			buffer,
			as_attachment=True,
			filename=f'Certificado_FER_{fer_info.ejercicio}_{fer_info.numcertificado:05d}.pdf',
			content_type='application/pdf'
		)
		
	except ImportError:
		messages.error(request, 'La librería ReportLab no está instalada. Por favor contacte al administrador.')
		return redirect('fer_asignacion_listado')
	except Exception as e:
		messages.error(request, f'Error al generar el certificado: {str(e)}')
		return redirect('fer_asignacion_listado')


@login_required
@require_http_methods(["GET"])
def fer_api_datos_grafico(request):
	"""API AJAX para obtener datos del gráfico de aplicación de recursos"""
	try:
		ejercicio = request.GET.get('ejercicio', datetime.now().year)
		
		# Obtener fondo del año fiscal
		fondo_ejercicio = FerFondos.objects.filter(ejercicio=int(ejercicio)).first()
		if not fondo_ejercicio:
			return JsonResponse({'error': 'No hay fondo configurado para este año'}, status=404)
		
		# Calcular total asignado (estado=0)
		total_asignado = FerInformacion.objects.filter(
			ejercicio=int(ejercicio),
			estado=0
		).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
		
		fondo_disponible = fondo_ejercicio.fondo - total_asignado
		
		return JsonResponse({
			'fondo_total': float(fondo_ejercicio.fondo),
			'fondo_asignado': float(total_asignado),
			'fondo_disponible': float(fondo_disponible),
			'porcentaje_asignado': round((total_asignado / fondo_ejercicio.fondo * 100) if fondo_ejercicio.fondo > 0 else 0, 2),
			'porcentaje_disponible': round((fondo_disponible / fondo_ejercicio.fondo * 100) if fondo_ejercicio.fondo > 0 else 0, 2),
		})
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=400)
