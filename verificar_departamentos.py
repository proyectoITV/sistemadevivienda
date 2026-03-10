import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import PersonalDepartamento, PersonalDireccion

print("\n" + "="*80)
print("RESUMEN DE CARGA - TABLA PERSONAL_DEPARTAMENTO")
print("="*80)

dirs = PersonalDireccion.objects.all().order_by('iddireccion')
total_departamentos = 0

for d in dirs:
    count = PersonalDepartamento.objects.filter(iddireccion=d).count()
    total_departamentos += count
    print(f"  {d.iddireccion}: {d.direccion:45s} - {count:2d} departamentos")

print("="*80)
print(f"Total de departamentos en la base de datos: {total_departamentos}")
print(f"Total de direcciones en la base de datos: {PersonalDireccion.objects.count()}")
print("="*80 + "\n")
