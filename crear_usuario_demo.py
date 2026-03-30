import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.models import PersonalEmpleados, PersonalDepartamento

# Obtener un departamento aleatorio
depts = PersonalDepartamento.objects.all()
dept = depts.first() if depts.exists() else None

# NOTA:
# El campo 'puesto' no existe en PersonalEmpleados.
# Usualmente el campo correcto es 'idpuesto' o similar.
# Cambia 'idpuesto' por el nombre real si es diferente.

usuario, creado = PersonalEmpleados.objects.get_or_create(
    usuario='demo',
    defaults={
        'email': 'demo@itavu.mx',
        'nombre_completo': 'Usuario de Prueba',
        'idpuesto': None,  # Cambia esto si tienes un puesto específico
        'iddepartamento': dept,
        'is_staff': True,
        'is_admin': True,
        'is_superuser': True,
    }
)

if creado:
    usuario.set_password('Demo123456')
    usuario.save()
    print(f"✓ Usuario creado exitosamente")
    print(f"  Usuario: demo")
    print(f"  Contraseña: Demo123456")
    print(f"  Email: demo@itavu.mx")
else:
    print(f"• Usuario ya existe")
    print(f"  Usuario: demo")