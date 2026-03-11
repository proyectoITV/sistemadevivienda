#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script para cargar datos iniciales del módulo FER
Ejecutar: python manage.py shell < cargar_datos_fer.py
"""

from portal.models import CatalogosSexo, FerFondos, FerCatSubsidio
from datetime import date

# Limpiar datos existentes
print("Limpiando datos existentes...")
CatalogosSexo.objects.all().delete()
FerCatSubsidio.objects.all().delete()
FerFondos.objects.all().delete()

# 1. Cargar Catálogos de Sexo
print("Cargando catálogos de sexos...")
sexos_data = [
    {'idsexo': 0, 'sexo': 'Ninguno'},
    {'idsexo': 1, 'sexo': 'Femenino'},
    {'idsexo': 2, 'sexo': 'Masculino'},
]

for sexo_data in sexos_data:
    sexo, created = CatalogosSexo.objects.get_or_create(
        sexo=sexo_data['sexo'],
        defaults={'activo': True}
    )
    status = "Creado" if created else "Existente"
    print(f"  - {sexo_data['sexo']}: {status}")

# 2. Cargar Catálogos de Subsidio
print("\nCargando catálogos de conceptos de subsidio...")
conceptos_data = [
    'Por descuento de Programa de Mejoramiento de Vivienda',
    'Por descuento de Programa de Vivienda',
    'Por descuento de Programa de Suelo Habitacional',
    'Por descuento de Costo de Regularización y/o Escrituración',
    'Por la condonación total del adeudo',
    'Por el descuento de Intereses',
    'Por el concepto de Cesión de Derechos',
]

for idx, concepto in enumerate(conceptos_data, 1):
    concepto_obj, created = FerCatSubsidio.objects.get_or_create(
        fer_idcon=idx,
        defaults={
            'fer_descripcion': concepto,
            'activo': True
        }
    )
    status = "Creado" if created else "Existente"
    print(f"  {idx}. {concepto}: {status}")

# 3. Cargar Fondos por Año
print("\nCargando fondos por ejercicio fiscal...")
fondos_data = [
    {
        'fondo': 350000,
        'ejercicio': 2018,
        'fechainicio': date(2018, 1, 1),
        'fechafin': date(2018, 12, 31),
        'sustento': 'Como apoyo autorizado en la Junta de Gobierno, Acta de Sesión Ordinaria No. 63, punto de acuerdo número 10, con fecha 08 de Agosto de 2018'
    },
    {
        'fondo': 1500000,
        'ejercicio': 2019,
        'fechainicio': date(2019, 3, 7),
        'fechafin': date(2019, 12, 31),
        'sustento': 'Como apoyo autorizado en la Junta de Gobierno, Acta de Sesión Ordinaria No. 65, punto de acuerdo número 5, con fecha 07 de Marzo de 2019'
    },
    {
        'fondo': 1500000,
        'ejercicio': 2020,
        'fechainicio': date(2020, 3, 11),
        'fechafin': date(2020, 12, 31),
        'sustento': '2020: Acta de Sesión Ordinaria 69, - Oficio de Autorización CD/1765/20'
    },
    {
        'fondo': 1000000,
        'ejercicio': 2021,
        'fechainicio': date(2000, 1, 1),
        'fechafin': date(2021, 12, 31),
        'sustento': '2021: Acta de la H. Junta de Gobierno, Sesión Ordinaria 73, con fecha 08 de Abril del 2021'
    },
    {
        'fondo': 2000000,
        'ejercicio': 2022,
        'fechainicio': date(2022, 3, 28),
        'fechafin': date(2022, 9, 30),
        'sustento': 'Autorizado con el Acta 77 y el oficio CD/ITV/0017/2022, y oficio de ampliación de $500,000.00 CD/ITV/067/2022'
    },
    {
        'fondo': 5000000,
        'ejercicio': 2023,
        'fechainicio': date(2023, 5, 26),
        'fechafin': date(2028, 9, 30),
        'sustento': 'Autorizado con el Acta de Sesión Ordinaria No. 82, celebrada del 26 de mayo en el punto número 14 del orden del día CD/ITV/710/2023 7 de Junio 2023'
    },
    {
        'fondo': 5000000,
        'ejercicio': 2024,
        'fechainicio': date(2023, 5, 26),
        'fechafin': date(2028, 9, 30),
        'sustento': 'Autorizado con el Acta de Sesión Ordinaria No. 82, celebrada del 26 de mayo en el punto número 14 del orden del día CD/ITV/710/2023 7 de Junio 2023'
    },
    {
        'fondo': 5000000,
        'ejercicio': 2025,
        'fechainicio': date(2023, 5, 26),
        'fechafin': date(2028, 9, 30),
        'sustento': 'Autorizado con el Acta de Sesión Ordinaria No. 82, celebrada del 26 de mayo en el punto número 14 del orden del día CD/ITV/710/2023 7 de Junio 2023, Incremento 3 millones más oficio DG/10206/2025'
    },
    {
        'fondo': 5000000,
        'ejercicio': 2026,
        'fechainicio': date(2023, 5, 26),
        'fechafin': date(2028, 9, 30),
        'sustento': 'Autorizado con el Acta de Sesión Ordinaria No. 82, celebrada del 26 de mayo en el punto número 14 del orden del día CD/ITV/710/2023 7 de Junio 2023, Incremento 3 millones más oficio DG/10206/2025'
    },
]

for fondo_data in fondos_data:
    fondo, created = FerFondos.objects.get_or_create(
        ejercicio=fondo_data['ejercicio'],
        defaults={
            'fondo': fondo_data['fondo'],
            'fechainicio': fondo_data['fechainicio'],
            'fechafin': fondo_data['fechafin'],
            'sustento': fondo_data['sustento'],
            'activo': True
        }
    )
    status = "Creado" if created else "Existente"
    print(f"  Año {fondo_data['ejercicio']}: ${fondo_data['fondo']:,} - {status}")

print("\n✓ Datos iniciales cargados exitosamente")
print(f"✓ Sexos: {CatalogosSexo.objects.count()}")
print(f"✓ Conceptos de Subsidio: {FerCatSubsidio.objects.count()}")
print(f"✓ Fondos: {FerFondos.objects.count()}")
