#!/usr/bin/env python
"""
Script para cargar datos iniciales de patrimonio:
- Marcas
- Clasificaciones SERAP
- Clasificaciones de Contraloría
- Proveedores (ejemplo)
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import (
    CatalogosMarcas,
    PatrimonioClasificacionSerap,
    PatrimonioClasificacionContraloria,
    PatrimonioProveedor,
)

def cargar_marcas():
    """Cargar marcas comunes"""
    marcas_data = [
        {'nombre': 'HP', 'descripcion': 'Hewlett-Packard'},
        {'nombre': 'Dell', 'descripcion': 'Dell Technologies'},
        {'nombre': 'Lenovo', 'descripcion': 'Lenovo'},
        {'nombre': 'Asus', 'descripcion': 'Asus'},
        {'nombre': 'Apple', 'descripcion': 'Apple Inc.'},
        {'nombre': 'Canon', 'descripcion': 'Canon Inc.'},
        {'nombre': 'Epson', 'descripcion': 'Seiko Epson Corporation'},
        {'nombre': 'Samsung', 'descripcion': 'Samsung Electronics'},
        {'nombre': 'LG', 'descripcion': 'LG Electronics'},
        {'nombre': 'Xerox', 'descripcion': 'Xerox Corporation'},
        {'nombre': 'Office Depot', 'descripcion': 'Mobiliario de oficina'},
        {'nombre': 'Steelcase', 'descripcion': 'Mobiliario de oficina'},
    ]
    
    for marca_data in marcas_data:
        marca, created = CatalogosMarcas.objects.get_or_create(
            nombre=marca_data['nombre'],
            defaults={'descripcion': marca_data['descripcion']}
        )
        if created:
            print(f"✓ Marca creada: {marca.nombre}")
        else:
            print(f"- Marca ya existe: {marca.nombre}")


def cargar_clasificaciones_serap():
    """Cargar clasificaciones SERAP"""
    clasificaciones = [
        'Equipo de comunicación',
        'Equipo de computo',
        'Herramienta',
        'Mobiliario y equipo de oficina',
    ]
    
    for nombre in clasificaciones:
        clasificacion, created = PatrimonioClasificacionSerap.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': f'Clasificación SERAP: {nombre}'}
        )
        if created:
            print(f"✓ Clasificación SERAP creada: {clasificacion.nombre}")
        else:
            print(f"- Clasificación SERAP ya existe: {clasificacion.nombre}")


def cargar_clasificaciones_contraloria():
    """Cargar clasificaciones de Contraloría"""
    clasificaciones = [
        'Bien controlable',
        'Bien controlable - gasto',
        'Bien inventariable',
        'Bienes baja definitiva',
    ]
    
    for nombre in clasificaciones:
        clasificacion, created = PatrimonioClasificacionContraloria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': f'Clasificación de Contraloría: {nombre}'}
        )
        if created:
            print(f"✓ Clasificación Contraloría creada: {clasificacion.nombre}")
        else:
            print(f"- Clasificación Contraloría ya existe: {clasificacion.nombre}")


def cargar_proveedores():
    """Cargar algunos proveedores de ejemplo"""
    proveedores_data = [
        {
            'nombre': 'Ingram Micro',
            'rfc': 'IMG000101ABC',
            'telefono': '5550001111',
            'correo': 'ventas@ingrammicro.com',
            'persona_contacto': 'Juan Pérez',
        },
        {
            'nombre': 'Softland',
            'rfc': 'SOF000102XYZ',
            'telefono': '5550002222',
            'correo': 'contacto@softland.com',
            'persona_contacto': 'María García',
        },
        {
            'nombre': 'Grupo Econom',
            'rfc': 'GEC000103DEF',
            'telefono': '5550003333',
            'correo': 'ventas@grupoeconom.com',
            'persona_contacto': 'Carlos López',
        },
        {
            'nombre': 'Muebles Corporativos',
            'rfc': 'MUE000104GHI',
            'telefono': '5550004444',
            'correo': 'contacto@mueblescorp.com',
            'persona_contacto': 'Rosa Martínez',
        },
    ]
    
    for proveedor_data in proveedores_data:
        proveedor, created = PatrimonioProveedor.objects.get_or_create(
            nombre=proveedor_data['nombre'],
            defaults={
                'rfc': proveedor_data.get('rfc', ''),
                'telefono': proveedor_data.get('telefono', ''),
                'correo': proveedor_data.get('correo', ''),
                'persona_contacto': proveedor_data.get('persona_contacto', ''),
            }
        )
        if created:
            print(f"✓ Proveedor creado: {proveedor.nombre}")
        else:
            print(f"- Proveedor ya existe: {proveedor.nombre}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Cargando datos iniciales de Patrimonio...")
    print("="*60 + "\n")
    
    print("Cargando Marcas...")
    cargar_marcas()
    print()
    
    print("Cargando Clasificaciones SERAP...")
    cargar_clasificaciones_serap()
    print()
    
    print("Cargando Clasificaciones de Contraloría...")
    cargar_clasificaciones_contraloria()
    print()
    
    print("Cargando Proveedores...")
    cargar_proveedores()
    print()
    
    print("="*60)
    print("✓ Datos iniciales cargados exitosamente!")
    print("="*60 + "\n")
