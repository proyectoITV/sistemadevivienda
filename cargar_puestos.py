#!/usr/bin/env python
"""Script para cargar los puestos en la base de datos"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.models import PersonalPuestos

puestos = [
    'Sin especificar',
    'Analista',
    'Auxiliar',
    'Auxiliar Administrativo',
    'Auxiliar Contable',
    'Auxiliar de Mantenimiento',
    'Auxiliar General',
    'Auxiliar Jurídico',
    'Auxiliar Operativo',
    'Auxiliar Técnico',
    'Ayudante de Topógrafo',
    'Cajera',
    'Cajero',
    'Capturista',
    'Chofer',
    'Coordinador',
    'Delegado',
    'Director',
    'Director General',
    'Enlace Administrativo',
    'Intendente',
    'Jefe de Departamento',
    'Notificador',
    'Programador',
    'Secretaria',
    'Secretaria Paticular',
    'Subdirector',
    'Técnico en Mantto de Sist',
    'Técnico en Sistemas',
    'Topógrafo',
    'Velador',
]

print('\n=== CARGANDO PUESTOS ===\n')
for puesto_nombre in puestos:
    puesto, created = PersonalPuestos.objects.get_or_create(
        nombre=puesto_nombre,
        defaults={'activo': True}
    )
    if created:
        print(f'✓ Creado: {puesto.nombre}')
    else:
        print(f'→ Ya existe: {puesto.nombre}')

total = PersonalPuestos.objects.count()
print(f'\n✓ Total de puestos: {total}\n')
