#!/usr/bin/env python
"""
Test si la migración se puede aplicar
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from anuncios.models import ColaCorreos
from django.core.management import call_command

print("=" * 80)
print("VERIFICACIÓN DE MIGRACIÓN 0018")
print("=" * 80)

try:
    # Verificar si el modelo existe
    count = ColaCorreos.objects.count()
    print("\n✅ ÉXITO: El modelo ColaCorreos está disponible en la BD")
    print(f"   Total de registros: {count}")
    
    # Verificar estructura
    campos = [f.name for f in ColaCorreos._meta.fields]
    print(f"\n✅ Campos encontrados: {len(campos)}")
    for campo in campos:
        print(f"   - {campo}")
    
    print("\n✅ La migración 0018 se aplicó correctamente!")
    print("\nProximos pasos:")
    print("1. Ir a http://localhost:8000/seguridad/cola-correos/")
    print("2. Ver el monitor del sistema de cola de correos")
    print("3. Probar funcionalidades")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\nIntentando aplicar migración...")
    try:
        call_command('migrate', 'anuncios', '0018')
        print("✅ Migración aplicada exitosamente")
    except Exception as migrate_error:
        print(f"❌ Error al aplicar migración: {migrate_error}")
        sys.exit(1)
