import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from anuncios.models import PatrimonioClasificacionSerap, PatrimonioClasificacionContraloria

def cargar_clasificaciones_serap():
    """Carga las clasificaciones SERAP"""
    clasificaciones = [
        {'id': 1, 'nombre': 'Sin especificar'},
        {'id': 2, 'nombre': 'Crear nuevo formato SERAP'},
        {'id': 3, 'nombre': 'Mobiliario y Equipo de Oficina'},
        {'id': 4, 'nombre': 'Equipo de Comunicación'},
        {'id': 5, 'nombre': 'Equipo de Computo'},
        {'id': 6, 'nombre': 'Herramienta'},
    ]
    
    print("Cargando Clasificaciones SERAP...")
    for item in clasificaciones:
        obj, created = PatrimonioClasificacionSerap.objects.update_or_create(
            idclasificacion_serap=item['id'],
            defaults={
                'nombre': item['nombre'],
                'descripcion': f"Clasificación SERAP: {item['nombre']}",
                'activo': True
            }
        )
        if created:
            print(f"✓ Creada: {item['nombre']}")
        else:
            print(f"↻ Actualizada: {item['nombre']}")

def cargar_clasificaciones_contraloria():
    """Carga las clasificaciones de contraloría"""
    clasificaciones = [
        {'id': 0, 'nombre': 'BIEN INVENTARIABLE'},
        {'id': 1, 'nombre': 'BIEN CONTROLABLE'},
        {'id': 2, 'nombre': 'BIEN CONTROLABLE - GASTO'},
        {'id': 3, 'nombre': 'BIENES BAJA DEFINITIVA'},
    ]
    
    print("\nCargando Clasificaciones de Contraloría...")
    for item in clasificaciones:
        obj, created = PatrimonioClasificacionContraloria.objects.update_or_create(
            idclasificacion_contraloria=item['id'],
            defaults={
                'nombre': item['nombre'],
                'descripcion': f"Clasificación de Contraloría: {item['nombre']}",
                'activo': True
            }
        )
        if created:
            print(f"✓ Creada: {item['nombre']}")
        else:
            print(f"↻ Actualizada: {item['nombre']}")

if __name__ == '__main__':
    try:
        cargar_clasificaciones_serap()
        cargar_clasificaciones_contraloria()
        print("\n✅ Clasificaciones cargadas exitosamente!")
        
        # Mostrar resumen
        print(f"\nResumen:")
        print(f"- Clasificaciones SERAP: {PatrimonioClasificacionSerap.objects.count()}")
        print(f"- Clasificaciones Contraloría: {PatrimonioClasificacionContraloria.objects.count()}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
