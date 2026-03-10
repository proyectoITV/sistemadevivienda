#!/usr/bin/env python
"""
Script para cargar los tipos de contratación en la base de datos
Ejecutar: python manage.py shell < cargar_tipos_contratacion.py
"""

from anuncios.models import PersonalTipoDeContratacion

# Datos a insertar
tipos_contratacion = [
    {
        'nombre': 'Sindical',
        'descripcion': 'Contratación sindicalizada con protecciones laborales',
    },
    {
        'nombre': 'Extraordinario',
        'descripcion': 'Contratación extraordinaria para proyectos o períodos específicos',
    },
    {
        'nombre': 'Operativo',
        'descripcion': 'Contratación operativa para funciones operacionales',
    },
]

# Insertar tipos de contratación
for tipo_data in tipos_contratacion:
    tipo, created = PersonalTipoDeContratacion.objects.get_or_create(
        nombre=tipo_data['nombre'],
        defaults={
            'descripcion': tipo_data['descripcion'],
            'activo': True,
            'usuario_captura': 'admin',
            'usuario_modificacion': 'admin',
        }
    )
    if created:
        print(f"✓ Creado: {tipo.nombre}")
    else:
        print(f"→ Ya existe: {tipo.nombre}")

print("\n✓ Carga de tipos de contratación completada")
