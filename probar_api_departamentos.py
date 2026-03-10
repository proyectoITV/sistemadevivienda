#!/usr/bin/env python
"""
Script de prueba para verificar que la API de departamentos-por-direccion funciona
Ejecutar: python manage.py runserver
Luego abrir en el navegador: http://localhost:8000/api/departamentos-por-direccion/?iddireccion=1
"""

import os
import django
from django.test import Client
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import PersonalDireccion

client = Client()

print('\n=== PRUEBA DE API ===\n')

direcciones = PersonalDireccion.objects.filter(activo=True)[:3]

for direccion in direcciones:
    print(f'Probando: {direccion.direccion} (ID: {direccion.iddireccion})')
    
    # Hacer petición GET
    response = client.get(f'/api/departamentos-por-direccion/?iddireccion={direccion.iddireccion}')
    
    print(f'  Status: {response.status_code}')
    
    if response.status_code == 200:
        data = json.loads(response.content)
        count = len(data.get('departamentos', []))
        print(f'  ✓ Departamentos retornados: {count}')
        
        # Mostrar primeros 3
        for dept in data.get('departamentos', [])[:3]:
            print(f'    - {dept["departamento"]}')
        if count > 3:
            print(f'    ... y {count - 3} más')
    else:
        print(f'  ✗ Error: {response.content.decode()}')
    
    print()

print('\n=== FIN DE PRUEBA ===\n')
