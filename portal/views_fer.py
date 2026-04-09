# -*- coding: utf-8 -*-
"""
Vistas para el módulo de Fondo Económico de Reserva (FER)
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from datetime import datetime

from .models import (
	FerInformacion,
	FerFondos,
	FerCatSubsidio,
	CatalogosSexo,
	CatalogosAdministraciones,
)
from .forms import FerInformacionForm


@login_required
@require_http_methods(["GET"])
def fer_asignacion_listado(request):
	"""Vista de listado de asignaciones de FER (Asignación de Recurso)"""
	try:
		# Obtener administración seleccionada
		administracion_id = request.GET.get('administracion_id')
		administraciones = CatalogosAdministraciones.objects.order_by('-fechainicio')
		administracion_seleccionada = None
		if administracion_id:
			administracion_seleccionada = administraciones.filter(idadministracion=int(administracion_id)).first()
		if not administracion_seleccionada:
			administracion_seleccionada = administraciones.first()

		# Obtener registros dentro del rango de fechas de la administración seleccionada
		registros = FerInformacion.objects.none()
		total_aplicado = 0
		fondo_total = 0
		fondo_disponible = 0

		if administracion_seleccionada:
			# Filtrar registros por rango de autorizo_fecha (fechainicio a fechatermino)
			registros = FerInformacion.objects.filter(
				autorizo_fecha__gte=administracion_seleccionada.fechainicio,
				autorizo_fecha__lte=administracion_seleccionada.fechatermino,
				estado=0  # Solo activos
			).select_related('nfer_concepto', 'id_municipio', 'id_sexo').order_by('-ejercicio', '-numcertificado')

			# Obtener el fondo con el idfondo más alto dentro del rango de la administración
			# (usando los campos fechainicio/fechafin del fondo)
			fondo_ejercicio = FerFondos.objects.filter(
				fechainicio__gte=administracion_seleccionada.fechainicio,
				fechafin__lte=administracion_seleccionada.fechatermino,
				activo=True,
			).order_by('-idfondo').first()

			# Calcular totales basados en los registros filtrados por fecha
			total_aplicado = registros.aggregate(Sum('cantidad'))['cantidad__sum'] or 0
			fondo_total = fondo_ejercicio.fondo if fondo_ejercicio else 0
			fondo_disponible = fondo_total - total_aplicado

		# Configuración de paginación
		page_size = request.GET.get('page_size', 30)
		try:
			page_size = int(page_size)
			if page_size <= 0:
				page_size = 30
		except (ValueError, TypeError):
			page_size = 30

		page_number = request.GET.get('page', 1)
		paginator = Paginator(registros, page_size)
		page_obj = paginator.get_page(page_number)
		registros_paginados = page_obj.object_list

		context = {
			'registros': registros_paginados,
			'page_obj': page_obj,
			'administraciones': administraciones,
			'administracion_seleccionada': administracion_seleccionada,
			'total_aplicado': float(total_aplicado),
			'fondo_total': float(fondo_total),
			'fondo_disponible': float(fondo_disponible),
			'page_sizes': [10, 30, 50, 100],
			'current_page_size': page_size,
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
			# Establecer valores automáticos
			current_year = timezone.now().year
			fer_info.ejercicio = current_year
			
			# Calcular nfer_id para la administración actual y asegurar que no exista globalmente (PK)
			try:
				administracion_actual = CatalogosAdministraciones.objects.filter(
					fechainicio__lte=timezone.now().date(),
					fechatermino__gte=timezone.now().date()
				).first()
				if administracion_actual:
					last_nfer = FerInformacion.objects.filter(
						autorizo_fecha__gte=administracion_actual.fechainicio,
						autorizo_fecha__lte=administracion_actual.fechatermino
					).order_by('-nfer_id').first()
					candidate = (last_nfer.nfer_id + 1) if last_nfer else 1
					while FerInformacion.objects.filter(nfer_id=candidate).exists():
						candidate += 1
					fer_info.nfer_id = candidate
				else:
					last_global = FerInformacion.objects.order_by('-nfer_id').first()
					fer_info.nfer_id = (last_global.nfer_id + 1) if last_global else 1
			except Exception:
				fer_info.nfer_id = 1
			
			# Calcular numcertificado como máximo + 1 para el ejercicio actual donde estado=0
			try:
				last_cert = FerInformacion.objects.filter(
					ejercicio=current_year,
					estado=0
				).order_by('-numcertificado').first()
				fer_info.numcertificado = (last_cert.numcertificado + 1) if last_cert else 1
			except Exception:
				fer_info.numcertificado = 1
			
			# Establecer información de autorización
			fer_info.autorizo = request.user.nombre_completo
			fer_info.autorizo_fecha = timezone.now().date()
			fer_info.autorizo_hora = timezone.now().time()
			
			fer_info.idempmodifica = request.user.id_empleado
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
def fer_informacion_editar(request, nfer_id, ejercicio):
	"""Vista para editar registro de FER"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id, ejercicio=ejercicio)
	
	if request.method == 'POST':
		form = FerInformacionForm(request.POST, request.FILES, instance=fer_info)
		if form.is_valid():
			fer_info = form.save(commit=False)
			fer_info.idempmodifica = request.user.id_empleado
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
def fer_informacion_detalle(request, nfer_id, ejercicio):
	"""Vista para ver detalle completo del registro FER"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id, ejercicio=ejercicio)
	
	context = {
		'fer_info': fer_info,
	}
	return render(request, 'desarrollo/fer/detalle_fer.html', context)


@login_required
@require_http_methods(["POST"])
def fer_informacion_inactivar(request, nfer_id, ejercicio):
	"""Vista para marcar registro FER como inactivo"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id, ejercicio=ejercicio)
	
	fer_info.estado = 1  # Marcar como inactivo
	fer_info.idempmodifica = request.user.id_empleado
	fer_info.fechaultimamod = timezone.now().date()
	fer_info.save()
	
	messages.success(request, f'El registro del beneficiario "{fer_info.nombre}" ha sido marcado como inactivo.')
	return redirect('fer_asignacion_listado')


@login_required
@require_http_methods(["GET"])
def fer_certificado_generar(request, nfer_id, ejercicio):
	"""Vista para generar PDF del certificado de subsidio"""
	fer_info = get_object_or_404(FerInformacion, nfer_id=nfer_id, ejercicio=ejercicio)
	
	try:
		import os
		from django.conf import settings
		from reportlab.lib.pagesizes import letter
		from reportlab.lib import colors
		from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
		from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
		from reportlab.lib.units import inch, cm
		from io import BytesIO
		import qrcode
		from num2words import num2words
		
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
		
		style_center = ParagraphStyle(
			'Center',
			parent=styles['Normal'],
			fontSize=10,
			leading=14,
			alignment=1,
		)
		
		# Contenido del documento
		content = []
		
		# Header: Logo left, info right
		logotipo_img_path = os.path.join(settings.BASE_DIR, 'cop', 'logotipo.jpg')
		header_data = []
		if os.path.exists(logotipo_img_path):
			try:
				img = Image(logotipo_img_path, width=9.5*cm, height=1*cm)
				info_text = f"""Fecha: {fer_info.autorizo_fecha.strftime("%d/%m/%Y") if fer_info.autorizo_fecha else ""}<br/>
Delegación: {fer_info.id_municipio.nombre if fer_info.id_municipio else ""}<br/>
Número de contrato: {fer_info.contrato if fer_info.contrato else ""}"""
				info_para = Paragraph(info_text,style_normal)
				header_data = [[img, info_para]]
			except Exception:
				pass
		
		if header_data:
			header_table = Table(header_data, colWidths=[11*cm, 6*cm])
			header_table.setStyle(TableStyle([
				('VALIGN', (0,0), (-1,-1), 'TOP'),
				('ALIGN', (1,0), (1,0), 'RIGHT'),
			]))
			content.append(header_table)
			content.append(Spacer(1, 0.4*inch))
		
		content.append(Paragraph(
			'<b>CERTIFICADO DE SUBSIDIO ESTATAL</b>',
			style_title
		))
		
		content.append(Spacer(1, 0.4*inch))
		
		# New paragraph
		content.append(Paragraph(
			'El Gobierno del Estado de Tamaulipas, por conducto del Instituto Tamaulipeco de Vivienda y Urbanismo, a través de la Delegación de este municipio y dentro del programa de apoyo a las personas que en virtud de que les es imposible finiquitar el adeudo por cuestiones diversas, las cuales van desde desempleo hasta gastos no contemplados en dichas familias, como enfermedad o muerte de algún familiar, para ello se ha creado un Fondo Económico de Reserva.',
			style_normal
		))
		
		content.append(Spacer(1, 0.3*inch))
		
		# Centered subsidy number
		content.append(Paragraph(
			f'Otorga el presente subsidio con número: {fer_info.numcertificado}',
			style_center
		))
		
		content.append(Spacer(1, 0.3*inch))
		
		# Cantidad con letra
		cantidad = fer_info.cantidad or 0
		pesos = int(cantidad)
		centavos = int((cantidad - pesos) * 100)
		cantidad_letra = f"{num2words(pesos, lang='es')} pesos"
		if centavos > 0:
			cantidad_letra += f" {num2words(centavos, lang='es')} centavos"
		
		content.append(Paragraph(
			f'Por la condonación total del adeudo, que asciende a la cantidad de $ {cantidad:,.2f} ({cantidad_letra.upper()}) a:',
			style_center
		))
		
		content.append(Spacer(1, 0.5*inch))

		content.append(Paragraph(
			f'<b>C. {fer_info.nombre or "---"}</b>',
			style_center
		))
		
		content.append(Spacer(1, 0.5*inch))
		
		# Authorization paragraph
		content.append(Paragraph(
			'Autorizado con el Acta de Sesión Ordinaria No. 82, celebrada del 26 de mayo en el punto número 14 del orden del dia CD/ITV/710/2023 7 de Junio 2023',
			style_normal
		))
		
		content.append(Spacer(1, 1.2*inch))
		
		# Signature with line above
		signature_data = [
			['', 'Arq. Manuel Guillermo Treviño Cantu'],
			['', 'Director General']
		]
		signature_table = Table(signature_data, colWidths=[3*cm, 11*cm])
		signature_table.setStyle(TableStyle([
			('LINEABOVE', (1,0), (1,0), 1, colors.black),
			('ALIGN', (1,0), (1,0), 'CENTER'),
			('ALIGN', (1,1), (1,1), 'CENTER'),
			('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
		]))
		content.append(signature_table)
		
		content.append(Spacer(1, 0.9*inch))
		
		# QR at bottom right
		qr_data = f"Nombre: {fer_info.nombre or ''}\nContrato: {fer_info.contrato or ''}\nFecha Autorización: {fer_info.autorizo_fecha.strftime('%d/%m/%Y') if fer_info.autorizo_fecha else ''}\nMunicipio: {fer_info.id_municipio.nombre if fer_info.id_municipio else ''}"
		qr = qrcode.QRCode(version=1, box_size=10, border=5)
		qr.add_data(qr_data)
		qr.make(fit=True)
		qr_img = qr.make_image(fill='black', back_color='white')
		
		# Guardar QR temporalmente
		qr_buffer = BytesIO()
		qr_img.save(qr_buffer, format='PNG')
		qr_buffer.seek(0)
		
		# Table for QR at right
		# Definimos el ancho total de la tabla (11cm + 5cm = 16cm)
		table_width = 16*cm
		table_height = 3*cm # Aproximado según tu imagen

		qr_table_data = [['', Image(qr_buffer, width=3*cm, height=3*cm)]]
		qr_table = Table(qr_table_data, colWidths=[11*cm, 5*cm])
		qr_table.setStyle(TableStyle([
			('ALIGN', (1,0), (1,0), 'RIGHT'),
			('VALIGN', (1,0), (1,0), 'BOTTOM'),
		]))
		content.append(qr_table) 
		
		# Construir PDF
		doc.build(content)
		
		# Retornar PDF
		buffer.seek(0)
		numcertificado_val = fer_info.numcertificado if fer_info.numcertificado is not None else 0
		return FileResponse(
			buffer,
			as_attachment=True,
			filename=f'Certificado_FER_{fer_info.ejercicio}_{numcertificado_val:05d}.pdf',
			content_type='application/pdf'
		)
		
	except ImportError:
		messages.error(request, 'La librería ReportLab no está instalada. Por favor contacte al administrador.')
		return redirect('fer_asignacion_listado')
	except Exception as e:
		messages.error(request, f'Error al generar el certificado: {str(e)}')
		return redirect('fer_asignacion_listado')


@login_required
@login_required
@require_http_methods(["GET"])
def fer_api_datos_grafico(request):
	"""API AJAX para obtener datos del gráfico de aplicación de recursos"""
	try:
		administracion_id = request.GET.get('administracion_id')
		administraciones = CatalogosAdministraciones.objects.order_by('-fechainicio')
		administracion_seleccionada = None
		if administracion_id:
			administracion_seleccionada = administraciones.filter(idadministracion=int(administracion_id)).first()
		if not administracion_seleccionada:
			administracion_seleccionada = administraciones.first()

		# Determinar rango de fechas según administración seleccionada
		if administracion_seleccionada:
			start_date = administracion_seleccionada.fechainicio
			end_date = administracion_seleccionada.fechatermino
		else:
			start_date = datetime.now().date()
			end_date = start_date

		# Obtener fondo más reciente comprendido en el rango de la administración
		fondo_ejercicio = FerFondos.objects.filter(
			fechainicio__gte=start_date,
			fechafin__lte=end_date,
			activo=True,
		).order_by('-idfondo').first()
		if not fondo_ejercicio:
			return JsonResponse({'error': 'No hay fondo configurado para esta administración'}, status=404)

		# Calcular total aplicado (estado=0) dentro del periodo de la administración
		total_aplicado = FerInformacion.objects.filter(
			autorizo_fecha__gte=start_date,
			autorizo_fecha__lte=end_date,
			estado=0
		).aggregate(Sum('cantidad'))['cantidad__sum'] or 0

		fondo_disponible = fondo_ejercicio.fondo - total_aplicado

		return JsonResponse({
			'fondo_total': float(fondo_ejercicio.fondo),
			'fondo_aplicado': float(total_aplicado),
			'fondo_disponible': float(fondo_disponible),
			'porcentaje_aplicado': round((total_aplicado / fondo_ejercicio.fondo * 100) if fondo_ejercicio.fondo > 0 else 0, 2),
			'porcentaje_disponible': round((fondo_disponible / fondo_ejercicio.fondo * 100) if fondo_ejercicio.fondo > 0 else 0, 2),
		})
	except Exception as e:
		return JsonResponse({'error': str(e)}, status=400)
