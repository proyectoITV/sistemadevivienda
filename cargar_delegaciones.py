import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.models import CatalogosDelegaciones, CatalogosMunicipios

# Datos de delegaciones (nombre y municipio relacionado)
delegaciones_data = [
	('MATAMOROS', 'Matamoros'),
	('NUEVO LAREDO', 'Nuevo Laredo'),
	('REYNOSA', 'Reynosa'),
	('SAN FERNANDO', 'San Fernando'),
	('TAMPICO', 'Tampico'),
	('VICTORIA', 'Victoria'),  # Ciudad Victoria (Tula es la actual capital)
	('ALTAMIRA', 'Altamira'),
	('MIGUEL ALEMAN', 'Miguel Aleman'),  # También conocido como Miquihuana
	('RIO BRAVO', 'Río Bravo'),
	('VALLE HERMOSO', 'Valle de Hermoso'),
	('ALDAMA', 'Aldama'),
	('ABASOLO', 'Abasolo'),
	('EL MANTE', 'El Mante'),
	('JIMENEZ', 'Jiménez'),
	('SOTO LA MARINA', 'Soto la Marina'),
	('GONZALEZ', 'González'),
	('LLERA', 'Llera'),
	('CAMARGO', 'Camargo'),
	('CIUDAD MADERO', 'Ciudad Madero'),
	('XICOTENCATL', 'Xicoténcatl'),
	('TULA', 'Tula'),
	('VILLA DE CASAS', 'Casas'),
	('DIAZ ORDAZ', 'Gustavo Díaz Ordaz'),
	('JAUMAVE', 'Jáumave'),
]

tamaulipas = None
try:
	from portal.models import CatalogosEntidadesFederativas
	tamaulipas = CatalogosEntidadesFederativas.objects.get(nombre='Tamaulipas')
except:
	print("⚠ Tamaulipas no encontrado")

for nombre_delegacion, nombre_municipio in delegaciones_data:
	municipio = None
	try:
		municipio = CatalogosMunicipios.objects.get(nombre=nombre_municipio)
	except CatalogosMunicipios.DoesNotExist:
		print(f"⚠ Municipio '{nombre_municipio}' no encontrado")
	
	obj, created = CatalogosDelegaciones.objects.get_or_create(
		nombre=nombre_delegacion,
		defaults={
			'municipio': municipio,
			'telefono': '+52 (000) 0000-0000',
			'direccion': f'{nombre_delegacion}, Tamaulipas, México',
			'horario': 'Lunes a Viernes 8:00 - 17:00',
		}
	)
	
	if created:
		print(f"✓ Delegación '{nombre_delegacion}' creada")
	else:
		print(f"~ Delegación '{nombre_delegacion}' ya existe")

print("\n✓ Carga de delegaciones completada")
