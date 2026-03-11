import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.models import CatalogosEntidadesFederativas

# Datos de los 32 estados de México
estados = [
	('Aguascalientes', '01'),
	('Baja California', '02'),
	('Baja California Sur', '03'),
	('Campeche', '04'),
	('Coahuila de Zaragoza', '05'),
	('Colima', '06'),
	('Chiapas', '07'),
	('Chihuahua', '08'),
	('Ciudad de México', '09'),
	('Durango', '10'),
	('Guanajuato', '11'),
	('Guerrero', '12'),
	('Hidalgo', '13'),
	('Jalisco', '14'),
	('México', '15'),
	('Michoacán de Ocampo', '16'),
	('Morelos', '17'),
	('Nayarit', '18'),
	('Nuevo León', '19'),
	('Oaxaca', '20'),
	('Puebla', '21'),
	('Querétaro', '22'),
	('Quintana Roo', '23'),
	('San Luis Potosí', '24'),
	('Sinaloa', '25'),
	('Sonora', '26'),
	('Tabasco', '27'),
	('Tamaulipas', '28'),
	('Tlaxcala', '29'),
	('Veracruz de Ignacio de la Llave', '30'),
	('Yucatán', '31'),
	('Zacatecas', '32'),
]

for nombre, clave in estados:
	obj, created = CatalogosEntidadesFederativas.objects.get_or_create(
		nombre=nombre,
		defaults={'clave': clave}
	)
	if created:
		print(f"✓ {nombre} creado")
	else:
		print(f"~ {nombre} ya existe")

print("\n✓ Carga de estados completada")
