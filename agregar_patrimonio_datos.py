#!/usr/bin/env python
"""
Script para agregar marcas, clasificaciones y proveedores adicionales
después de la instalación inicial.

Uso:
    python agregar_patrimonio_datos.py
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


def agregar_marcas():
    """Agregar marcas adicionales"""
    print("\n=== Agregar Nuevas Marcas ===\n")
    
    marcas_nuevas = [
        {'nombre': 'Microsoft', 'descripcion': 'Microsoft Corporation'},
        {'nombre': 'Sony', 'descripcion': 'Sony Corporation'},
        {'nombre': 'Panasonic', 'descripcion': 'Panasonic Corporation'},
        {'nombre': 'Fujitsu', 'descripcion': 'Fujitsu Limited'},
    ]
    
    for marca_data in marcas_nuevas:
        marca, created = CatalogosMarcas.objects.get_or_create(
            nombre=marca_data['nombre'],
            defaults={'descripcion': marca_data['descripcion']}
        )
        if created:
            print(f"✓ Nueva marca: {marca.nombre}")
        else:
            print(f"- Marca ya existe: {marca.nombre}")


def agregar_clasificaciones_serap():
    """Agregar clasificaciones SERAP adicionales"""
    print("\n=== Agregar Clasificaciones SERAP ===\n")
    
    nuevas_clasificaciones = [
        'Vehículo',
        'Equipo de oficina',
        'Equipo de cómputo periférico',
        'Maquinaria',
    ]
    
    for nombre in nuevas_clasificaciones:
        clasificacion, created = PatrimonioClasificacionSerap.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': f'Clasificación SERAP: {nombre}'}
        )
        if created:
            print(f"✓ Nueva clasificación SERAP: {clasificacion.nombre}")
        else:
            print(f"- Clasificación ya existe: {clasificacion.nombre}")


def agregar_clasificaciones_contraloria():
    """Agregar clasificaciones de Contraloría adicionales"""
    print("\n=== Agregar Clasificaciones de Contraloría ===\n")
    
    nuevas_clasificaciones = [
        'Bien no fungible',
        'Bien consumible',
        'Bien sujeto a vigilancia',
    ]
    
    for nombre in nuevas_clasificaciones:
        clasificacion, created = PatrimonioClasificacionContraloria.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': f'Clasificación de Contraloría: {nombre}'}
        )
        if created:
            print(f"✓ Nueva clasificación Contraloría: {clasificacion.nombre}")
        else:
            print(f"- Clasificación ya existe: {clasificacion.nombre}")


def agregar_proveedores():
    """Agregar proveedores adicionales"""
    print("\n=== Agregar Nuevos Proveedores ===\n")
    
    nuevos_proveedores = [
        {
            'nombre': 'Best Buy',
            'rfc': 'BES000501ABC',
            'telefono': '5550005555',
            'correo': 'compras@bestbuy.com',
            'persona_contacto': 'Roberto García',
        },
        {
            'nombre': 'Costco',
            'rfc': 'COS000502DEF',
            'telefono': '5550006666',
            'correo': 'ventas@costco.com',
            'persona_contacto': 'Patricia López',
        },
        {
            'nombre': 'Amazon Business',
            'rfc': 'AMZ000503GHI',
            'telefono': '5550007777',
            'correo': 'contacto@amazon.com',
            'persona_contacto': 'Fernando Martínez',
        },
    ]
    
    for proveedor_data in nuevos_proveedores:
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
            print(f"✓ Nuevo proveedor: {proveedor.nombre}")
        else:
            print(f"- Proveedor ya existe: {proveedor.nombre}")


def listar_datos():
    """Mostrar todos los datos cargados"""
    print("\n=== RESUMEN DE DATOS CARGADOS ===\n")
    
    marcas = CatalogosMarcas.objects.filter(activo=True)
    print(f"Marcas activas: {marcas.count()}")
    for marca in marcas:
        print(f"  • {marca.nombre}")
    
    serap = PatrimonioClasificacionSerap.objects.filter(activo=True)
    print(f"\nClasificaciones SERAP: {serap.count()}")
    for c in serap:
        print(f"  • {c.nombre}")
    
    contraloria = PatrimonioClasificacionContraloria.objects.filter(activo=True)
    print(f"\nClasificaciones Contraloría: {contraloria.count()}")
    for c in contraloria:
        print(f"  • {c.nombre}")
    
    proveedores = PatrimonioProveedor.objects.filter(activo=True)
    print(f"\nProveedores activos: {proveedores.count()}")
    for p in proveedores:
        print(f"  • {p.nombre}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Agregar Datos Adicionales a Patrimonio")
    print("="*60)
    
    agregar_marcas()
    agregar_clasificaciones_serap()
    agregar_clasificaciones_contraloria()
    agregar_proveedores()
    
    listar_datos()
    
    print("\n" + "="*60)
    print("✓ Datos adicionales agregados exitosamente!")
    print("="*60 + "\n")
