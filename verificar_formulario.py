#!/usr/bin/env python
"""Script para verificar que el formulario tiene el campo correcto"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.forms import PersonalEmpleadosForm

form = PersonalEmpleadosForm()
print('\n=== CAMPOS DEL FORMULARIO ===\n')
for field_name, field in form.fields.items():
    print(f'{field_name}: {field.__class__.__name__}')
    
print('\n=== CAMPO TIPO DE CONTRATACIÓN ===')
tc_field = form.fields.get('idtipodecontratacion')
if tc_field:
    print(f'✓ Campo encontrado: {tc_field}')
    print(f'Tipo: {tc_field.__class__.__name__}')
    print(f'Widget: {tc_field.widget.__class__.__name__}')
    if hasattr(tc_field, 'queryset'):
        print(f'Opciones: {list(tc_field.queryset.values_list("nombre", flat=True))}')
else:
    print('✗ Campo NO encontrado')

print('\n')
