#!/usr/bin/env python
"""Script para verificar los campos del formulario actualizado"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.forms import PersonalEmpleadosForm
from portal.models import PersonalPuestos, PersonalTipoDeContratacion

form = PersonalEmpleadosForm()

print('\n=== VERIFICACIÓN DE CAMPOS DEL FORMULARIO ===\n')

# Verificar campo de puesto
puesto_field = form.fields.get('idpuesto')
if puesto_field:
    print(f'✓ Campo PUESTO encontrado')
    print(f'  Tipo: {puesto_field.__class__.__name__}')
    print(f'  Widget: {puesto_field.widget.__class__.__name__}')
    if hasattr(puesto_field, 'queryset'):
        count = puesto_field.queryset.count()
        print(f'  Total de puestos en BD: {count}')
        print(f'  Primeros 5: {list(puesto_field.queryset.values_list("nombre", flat=True)[:5])}')
else:
    print('✗ Campo PUESTO NO encontrado')

print()

# Verificar campo de tipo de contratación
tc_field = form.fields.get('idtipodecontratacion')
if tc_field:
    print(f'✓ Campo TIPO DE CONTRATACIÓN encontrado')
    print(f'  Tipo: {tc_field.__class__.__name__}')
    print(f'  Widget: {tc_field.widget.__class__.__name__}')
    if hasattr(tc_field, 'queryset'):
        count = tc_field.queryset.count()
        print(f'  Total de tipos en BD: {count}')
        print(f'  Opciones: {list(tc_field.queryset.values_list("nombre", flat=True))}')
else:
    print('✗ Campo TIPO DE CONTRATACIÓN NO encontrado')

print('\n')
