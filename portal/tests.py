from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import ViaticosSolicitudForm
from .models import (
	PersonalDepartamento,
	PersonalDireccion,
	PersonalEmpleados,
	ViaticosPresupuestoDireccion,
	ViaticosSolicitud,
	ViaticosUbicacion,
	ViaticosZonaTarifa,
)


class ViaticosTests(TestCase):
	def setUp(self):
		self.direccion = PersonalDireccion.objects.create(direccion='DIRECCION DE ADMINISTRACION Y FINANZAS')
		self.departamento = PersonalDepartamento.objects.create(
			departamento='DEPARTAMENTO DE RECURSOS MATERIALES',
			iddireccion=self.direccion,
		)
		self.empleado = PersonalEmpleados.objects.create(
			email='viaticos@itavu.mx',
			apellido_paterno='Perez',
			apellido_materno='Lopez',
			nombre='Maria',
			iddepartamento=self.departamento,
			numero_empleado='A-100',
			curp='PELM900101MTSRRA01',
			rfc='PELM900101AB1',
		)
		self.zona, _ = ViaticosZonaTarifa.objects.update_or_create(
			clave=ViaticosZonaTarifa.ZONA_NORTE,
			defaults={
				'nombre': 'Zona Norte',
				'hospedaje_noche': Decimal('1600.00'),
				'alimentacion_diaria': Decimal('425.00'),
				'combustible_km': Decimal('3.7500'),
				'activo': True,
			}
		)
		self.presupuesto = ViaticosPresupuestoDireccion.objects.create(
			iddireccion=self.direccion,
			ejercicio=timezone.localdate().year,
			monto_asignado=Decimal('50000.00'),
		)
		self.admin = PersonalEmpleados.objects.create(
			email='admin.viaticos@itavu.mx',
			apellido_paterno='Admin',
			apellido_materno='Sistema',
			nombre='Control',
			iddepartamento=self.departamento,
			numero_empleado='A-101',
			curp='AASC900101HTSRNL02',
			rfc='AASC900101AB2',
			is_superuser=True,
			is_staff=True,
		)

	def test_viatico_recalcula_total_estimado_con_vehiculo(self):
		viatico = ViaticosSolicitud.objects.create(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Supervision regional',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Reynosa, Tamaulipas',
			distancia_km=Decimal('120.00'),
			viaje_redondo=True,
			dias=3,
			transporte=ViaticosSolicitud.TRANSPORTE_VEHICULO,
			pasajes_estimados=Decimal('0.00'),
			taxis_estimados=Decimal('300.00'),
		)

		self.assertEqual(viatico.hospedaje_estimado, Decimal('3200.00'))
		self.assertEqual(viatico.alimentacion_estimada, Decimal('1275.00'))
		self.assertEqual(viatico.combustible_estimado, Decimal('900.00'))
		self.assertEqual(viatico.total_estimado, Decimal('5675.00'))

	def test_viatico_no_permite_exceder_presupuesto_disponible(self):
		ViaticosSolicitud.objects.create(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Comision principal',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Matamoros, Tamaulipas',
			distancia_km=Decimal('1000.00'),
			viaje_redondo=True,
			dias=7,
			transporte=ViaticosSolicitud.TRANSPORTE_VEHICULO,
			pasajes_estimados=Decimal('0.00'),
			taxis_estimados=Decimal('1000.00'),
		)

		segundo = ViaticosSolicitud(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Comision adicional',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Nuevo Laredo, Tamaulipas',
			distancia_km=Decimal('2600.00'),
			viaje_redondo=True,
			dias=7,
			transporte=ViaticosSolicitud.TRANSPORTE_VEHICULO,
			pasajes_estimados=Decimal('0.00'),
			taxis_estimados=Decimal('750.00'),
		)

		with self.assertRaises(ValidationError):
			segundo.full_clean()

	def test_form_infiere_presupuesto_desde_direccion_del_empleado(self):
		form = ViaticosSolicitudForm(data={
			'empleado': self.empleado.pk,
			'zona': self.zona.pk,
			'motivo_comision': 'Revision administrativa',
			'origen': 'Ciudad Victoria, Tamaulipas',
			'destino': 'Tampico, Tamaulipas',
			'origen_latitud': '',
			'origen_longitud': '',
			'destino_latitud': '',
			'destino_longitud': '',
			'distancia_km': '50',
			'viaje_redondo': 'on',
			'dias': '2',
			'transporte': ViaticosSolicitud.TRANSPORTE_AUTOBUS,
			'pasajes_estimados': '1200.00',
			'taxis_estimados': '100.00',
			'observaciones': '',
		})

		self.assertTrue(form.is_valid(), form.errors)
		instancia = form.save(commit=False)
		self.assertEqual(instancia.presupuesto, self.presupuesto)
		self.assertEqual(instancia.direccion, self.direccion)

	def test_registrar_ubicacion_actualiza_ultimo_punto_y_historial(self):
		viatico = ViaticosSolicitud.objects.create(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Seguimiento operativo',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Tampico, Tamaulipas',
			distancia_km=Decimal('250.00'),
			viaje_redondo=False,
			dias=2,
			transporte=ViaticosSolicitud.TRANSPORTE_AUTOBUS,
			pasajes_estimados=Decimal('900.00'),
			taxis_estimados=Decimal('150.00'),
		)

		ubicacion = viatico.registrar_ubicacion(
			empleado=self.empleado,
			latitud=Decimal('23.741200'),
			longitud=Decimal('-99.145300'),
			precision_metros=Decimal('12.50'),
			velocidad_kmh=Decimal('41.20'),
		)

		viatico.refresh_from_db()
		self.assertTrue(viatico.seguimiento_activo)
		self.assertEqual(viatico.ultima_latitud, Decimal('23.741200'))
		self.assertEqual(viatico.ultima_longitud, Decimal('-99.145300'))
		self.assertEqual(viatico.ultima_precision_metros, Decimal('12.50'))
		self.assertEqual(viatico.ultima_velocidad_kmh, Decimal('41.20'))
		self.assertEqual(ViaticosUbicacion.objects.filter(viatico=viatico).count(), 1)
		self.assertEqual(ubicacion.empleado, self.empleado)

	def test_api_actualizar_ubicacion_viatico_regresa_ok(self):
		viatico = ViaticosSolicitud.objects.create(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Comision con rastreo',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Matamoros, Tamaulipas',
			distancia_km=Decimal('320.00'),
			viaje_redondo=False,
			dias=2,
			transporte=ViaticosSolicitud.TRANSPORTE_AUTOBUS,
			pasajes_estimados=Decimal('1500.00'),
			taxis_estimados=Decimal('200.00'),
		)

		self.client.force_login(self.empleado)
		response = self.client.post(
			reverse('actualizar_ubicacion_viatico', args=[viatico.id]),
			data={
				'latitud': '23.700100',
				'longitud': '-99.120200',
				'precision_metros': '9.80',
				'velocidad_kmh': '63.10',
			},
		)

		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertTrue(payload['success'])
		self.assertIn('google_maps_url', payload)
		viatico.refresh_from_db()
		self.assertEqual(viatico.ultima_latitud, Decimal('23.700100'))

	def test_api_posiciones_viaticos_lista_solo_seguimientos_activos(self):
		viatico = ViaticosSolicitud.objects.create(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Supervision cartografica',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Nuevo Laredo, Tamaulipas',
			distancia_km=Decimal('450.00'),
			viaje_redondo=False,
			dias=3,
			transporte=ViaticosSolicitud.TRANSPORTE_VEHICULO,
			pasajes_estimados=Decimal('0.00'),
			taxis_estimados=Decimal('150.00'),
		)
		viatico.registrar_ubicacion(
			empleado=self.empleado,
			latitud=Decimal('23.730000'),
			longitud=Decimal('-99.130000'),
		)

		self.client.force_login(self.admin)
		response = self.client.get(reverse('api_posiciones_viaticos'))

		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertEqual(len(payload['items']), 1)
		self.assertEqual(payload['items'][0]['id'], viatico.id)

	def test_api_recorrido_viatico_regresa_historial_ordenado(self):
		viatico = ViaticosSolicitud.objects.create(
			empleado=self.empleado,
			direccion=self.direccion,
			presupuesto=self.presupuesto,
			zona=self.zona,
			motivo_comision='Comision con reproducción',
			origen='Ciudad Victoria, Tamaulipas',
			destino='Tampico, Tamaulipas',
			distancia_km=Decimal('240.00'),
			viaje_redondo=False,
			dias=2,
			transporte=ViaticosSolicitud.TRANSPORTE_AUTOBUS,
			pasajes_estimados=Decimal('1000.00'),
			taxis_estimados=Decimal('120.00'),
		)
		primera = viatico.registrar_ubicacion(
			empleado=self.empleado,
			latitud=Decimal('23.741200'),
			longitud=Decimal('-99.145300'),
		)
		segunda = viatico.registrar_ubicacion(
			empleado=self.empleado,
			latitud=Decimal('22.255300'),
			longitud=Decimal('-97.868600'),
			velocidad_kmh=Decimal('82.40'),
		)

		self.client.force_login(self.admin)
		response = self.client.get(reverse('api_recorrido_viatico', args=[viatico.id]))

		self.assertEqual(response.status_code, 200)
		payload = response.json()
		self.assertTrue(payload['success'])
		self.assertEqual(len(payload['items']), 2)
		self.assertEqual(payload['items'][0]['id'], primera.id)
		self.assertEqual(payload['items'][1]['id'], segunda.id)
		self.assertEqual(payload['viatico']['folio'], viatico.folio)
