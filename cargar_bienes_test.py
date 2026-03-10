#!/usr/bin/env python
"""Script para cargar bienes de prueba"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import (
    PatrimonioBienesDelInstituto, CatalogosMarcas, PatrimonioProveedor,
    PatrimonioClasificacionSerap, PatrimonioClasificacionContraloria
)

print("=== CARGANDO BIENES DE PRUEBA ===\n")

# Obtener referencias
marca_dell = CatalogosMarcas.objects.filter(nombre='Dell').first()
marca_hp = CatalogosMarcas.objects.filter(nombre='HP').first()
proveedor = PatrimonioProveedor.objects.first()
serap = PatrimonioClasificacionSerap.objects.first()
contraloria = PatrimonioClasificacionContraloria.objects.first()

if not all([marca_dell, marca_hp, proveedor, serap, contraloria]):
    print("❌ Error: No existen los registros base necesarios")
    exit(1)

# Bien 1: Monitor Dell
bien1_data = {
    'numero_inventario_itavu': 'ITAVU-2026-001',
    'numero_inventario_gobierno': 'GOB-2026-001',
    'descripcion': 'Monitor Dell UltraSharp 27 pulgadas',
    'marca': marca_dell,
    'modelo': 'U2720Q',
    'serie': 'SN123456789',
    'fecha_factura': date(2025, 1, 15),
    'numero_factura': 'FAC-2025-001',
    'costo_articulo': 3500.00,
    'proveedor': proveedor,
    'clasificacion_serap': serap,
    'clasificacion_contraloria': contraloria,
    'observaciones': 'Bien de prueba 1 - Monitor en buenas condiciones',
    'activo': True,
    'usuario_captura': 'admin'
}

bien2_data = {
    'numero_inventario_itavu': 'ITAVU-2026-002',
    'numero_inventario_gobierno': 'GOB-2026-002',
    'descripcion': 'Impresora HP LaserJet Pro M404n',
    'marca': marca_hp,
    'modelo': 'M404n',
    'serie': 'SN987654321',
    'fecha_factura': date(2025, 1, 20),
    'numero_factura': 'FAC-2025-002',
    'costo_articulo': 2800.00,
    'proveedor': proveedor,
    'clasificacion_serap': serap,
    'clasificacion_contraloria': contraloria,
    'observaciones': 'Bien de prueba 2 - Impresora funcionando correctamente',
    'activo': True,
    'usuario_captura': 'admin'
}

# Verificar si ya existen
if PatrimonioBienesDelInstituto.objects.filter(numero_inventario_itavu='ITAVU-2026-001').exists():
    print("⚠️  El bien ITAVU-2026-001 ya existe, saltando...")
else:
    PatrimonioBienesDelInstituto.objects.create(**bien1_data)
    print("✓ Agregado: ITAVU-2026-001 (Monitor Dell)")

if PatrimonioBienesDelInstituto.objects.filter(numero_inventario_itavu='ITAVU-2026-002').exists():
    print("⚠️  El bien ITAVU-2026-002 ya existe, saltando...")
else:
    PatrimonioBienesDelInstituto.objects.create(**bien2_data)
    print("✓ Agregado: ITAVU-2026-002 (Impresora HP)")

total = PatrimonioBienesDelInstituto.objects.count()
print(f"\n✅ Total de bienes en la base de datos: {total}")
