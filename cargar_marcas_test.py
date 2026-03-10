#!/usr/bin/env python
"""Script para cargar datos de prueba de marcas, proveedores y clasificaciones"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import CatalogosMarcas, PatrimonioProveedor, PatrimonioClasificacionSerap, PatrimonioClasificacionContraloria

# Cargar marcas
print("=== CARGANDO MARCAS ===")
if CatalogosMarcas.objects.count() == 0:
    marcas = ['Dell', 'HP', 'Lenovo', 'Asus', 'Apple', 'Samsung', 'LG', 'Sony', 'Canon', 'Epson']
    for marca in marcas:
        CatalogosMarcas.objects.create(nombre=marca)
    print(f"✓ Agregadas {len(marcas)} marcas")
else:
    print(f"✓ Ya hay {CatalogosMarcas.objects.count()} marcas")

# Cargar proveedores
print("\n=== CARGANDO PROVEEDORES ===")
if PatrimonioProveedor.objects.count() == 0:
    proveedores = [
        {'nombre': 'Distribuidor Central', 'rfc': 'DICC123456XYZ'},
        {'nombre': 'Tech Solutions', 'rfc': 'TECH234567XYZ'},
        {'nombre': 'Office Depot', 'rfc': 'OFDE345678XYZ'},
        {'nombre': 'Staples', 'rfc': 'STAP456789XYZ'},
        {'nombre': 'Proveedora Tamaulipas', 'rfc': 'PRTM567890XYZ'}
    ]
    for proveedor in proveedores:
        PatrimonioProveedor.objects.create(**proveedor)
    print(f"✓ Agregados {len(proveedores)} proveedores")
else:
    print(f"✓ Ya hay {PatrimonioProveedor.objects.count()} proveedores")

# Cargar clasificaciones SERAP
print("\n=== CARGANDO CLASIFICACIONES SERAP ===")
if PatrimonioClasificacionSerap.objects.count() == 0:
    seraps = ['Equipo de Computo', 'Equipo de Comunicación', 'Herramienta', 'Mobiliario y Equipo de Oficina', 'Sin especificar']
    for nombre in seraps:
        PatrimonioClasificacionSerap.objects.create(nombre=nombre)
    print(f"✓ Agregadas {len(seraps)} clasificaciones SERAP")
else:
    print(f"✓ Ya hay {PatrimonioClasificacionSerap.objects.count()} clasificaciones SERAP")

# Cargar clasificaciones Contraloría
print("\n=== CARGANDO CLASIFICACIONES CONTRALORÍA ===")
if PatrimonioClasificacionContraloria.objects.count() == 0:
    controloria = ['BIEN CONTROLABLE', 'BIEN CONTROLABLE - GASTO', 'BIEN INVENTARIABLE', 'BIENES BAJA DEFINITIVA']
    for nombre in controloria:
        PatrimonioClasificacionContraloria.objects.create(nombre=nombre)
    print(f"✓ Agregadas {len(controloria)} clasificaciones Contraloría")
else:
    print(f"✓ Ya hay {PatrimonioClasificacionContraloria.objects.count()} clasificaciones Contraloría")

print("\n✅ TODOS LOS DATOS HAN SIDO CARGADOS CORRECTAMENTE")
