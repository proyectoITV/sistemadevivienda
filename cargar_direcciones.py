import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import PersonalDireccion

# Datos de direcciones a cargar
DIRECCIONES = [
    'DIRECCION GENERAL',
    'COORDINACION DE DELEGACIONES',
    'DIRECCION DE PLANEACION Y EVALUACION',
    'DIRECCION JURIDICA Y SEGURIDAD PATRIMONIAL',
    'DIRECCION DE PROGRAMAS DE SUELO Y VIVIENDA',
    'DIRECCION DE ADMINISTRACION Y FINANZAS',
]

def cargar_direcciones():
    """Carga las direcciones iniciales en la tabla personal_direccion"""
    
    direcciones_cargadas = 0
    direcciones_existentes = 0
    
    for direccion in DIRECCIONES:
        obj, creado = PersonalDireccion.objects.get_or_create(
            direccion=direccion,
            defaults={
                'activo': True,
                'usuario_captura': 'SISTEMA',
                'usuario_modificacion': 'SISTEMA',
            }
        )
        
        if creado:
            print(f"✓ Dirección creada: {direccion}")
            direcciones_cargadas += 1
        else:
            print(f"• Dirección ya existe: {direccion}")
            direcciones_existentes += 1
    
    print(f"\n{'='*60}")
    print(f"Resumen:")
    print(f"  Direcciones nuevas cargadas: {direcciones_cargadas}")
    print(f"  Direcciones que ya existían: {direcciones_existentes}")
    print(f"  Total de direcciones en la BD: {PersonalDireccion.objects.count()}")
    print(f"{'='*60}")

if __name__ == '__main__':
    cargar_direcciones()
