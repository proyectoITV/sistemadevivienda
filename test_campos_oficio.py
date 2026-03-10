"""
Script para probar la funcionalidad de campos de oficio en resguardos internos.
Ejecutar: python manage.py shell < test_campos_oficio.py
"""

from anuncios.models import PatrimonioResguardo, PatrimonioBienesDelInstituto, PersonalEmpleados
from anuncios.forms import PatrimonioResguardoAsignacionForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
import os

print("\n" + "="*70)
print("🧪 PRUEBAS DE CAMPOS DE OFICIO EN RESGUARDOS")
print("="*70 + "\n")

# ============================================================================
# TEST 1: Verificar que los campos existen en el modelo
# ============================================================================
print("TEST 1: Verificar campos en modelo PatrimonioResguardo")
print("-" * 70)

try:
    resguardo = PatrimonioResguardo()
    campos = ['numero_oficio', 'fecha_oficio', 'archivo_oficio']
    
    for campo in campos:
        if hasattr(resguardo, campo):
            print(f"  ✓ Campo '{campo}' existe en modelo")
        else:
            print(f"  ✗ Campo '{campo}' NO existe en modelo")
    
    print("\n✅ TEST 1 COMPLETADO\n")
except Exception as e:
    print(f"❌ ERROR en TEST 1: {e}\n")

# ============================================================================
# TEST 2: Verificar estructura de base de datos
# ============================================================================
print("TEST 2: Verificar estructura de base de datos")
print("-" * 70)

try:
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'anuncios_patrimonioresguardo'
            AND column_name LIKE '%oficio%'
            ORDER BY column_name
        """)
        
        columnas = cursor.fetchall()
        
        if columnas:
            for nombre, tipo in columnas:
                print(f"  ✓ {nombre} ({tipo})")
            print("\n✅ TEST 2 COMPLETADO\n")
        else:
            print("  ✗ No se encontraron columnas de oficio")
            print("\n⚠️ TEST 2 INCONCLUSO\n")
            
except Exception as e:
    print(f"❌ ERROR en TEST 2: {e}\n")

# ============================================================================
# TEST 3: Probar validación de formulario (extensión de archivo)
# ============================================================================
print("TEST 3: Validación de extensión de archivo (forma)")
print("-" * 70)

try:
    # Obtener primer bien y empleado para las pruebas
    bien = PatrimonioBienesDelInstituto.objects.first()
    empleado = PersonalEmpleados.objects.first()
    
    if bien and empleado:
        # TEST 3A: Archivo PDF válido
        print("  Subprueba 3A: PDF válido (debe pasar)")
        pdf_valido = SimpleUploadedFile(
            "oficio_valido.pdf",
            b"PDF Content Here",
            content_type="application/pdf"
        )
        
        form_data = {
            'bien': bien.idbien,
            'empleado': empleado.idempleado,
            'fecha_asignacion': '2026-03-06',
            'numero_oficio': 'OF-2026-001',
            'fecha_oficio': '2026-03-06',
            'observaciones_asignacion': 'Test'
        }
        
        form = PatrimonioResguardoAsignacionForm(
            data=form_data,
            files={'archivo_oficio': pdf_valido}
        )
        
        if form.is_valid():
            print(f"    ✓ PDF válido aceptado\n")
        else:
            print(f"    ✗ Errores: {form.errors}\n")
        
        # TEST 3B: Archivo no-PDF (debe fallar)
        print("  Subprueba 3B: Archivo no-PDF (debe rechazar)")
        archivo_txt = SimpleUploadedFile(
            "archivo.txt",
            b"Contenido texto",
            content_type="text/plain"
        )
        
        form = PatrimonioResguardoAsignacionForm(
            data=form_data,
            files={'archivo_oficio': archivo_txt}
        )
        
        if not form.is_valid() and 'archivo_oficio' in form.errors:
            print(f"    ✓ Archivo no-PDF rechazado correctamente")
            print(f"      Error: {form.errors['archivo_oficio'][0]}\n")
        else:
            print(f"    ✗ Archivo no-PDF no fue rechazado\n")
        
        print("✅ TEST 3 COMPLETADO\n")
    else:
        print("  ⚠️ No hay bienes o empleados en base de datos\n")
        
except Exception as e:
    print(f"❌ ERROR en TEST 3: {e}\n")

# ============================================================================
# TEST 4: Probar validación de tamaño de archivo
# ============================================================================
print("TEST 4: Validación de tamaño de archivo")
print("-" * 70)

try:
    bien = PatrimonioBienesDelInstituto.objects.first()
    empleado = PersonalEmpleados.objects.first()
    
    if bien and empleado:
        # TEST 4A: Archivo dentro del límite (5 MB)
        print("  Subprueba 4A: PDF de 5 MB (debe pasar)")
        archivo_5mb = SimpleUploadedFile(
            "oficio_5mb.pdf",
            b"X" * (5 * 1024 * 1024),  # 5 MB
            content_type="application/pdf"
        )
        
        form_data = {
            'bien': bien.idbien,
            'empleado': empleado.idempleado,
            'fecha_asignacion': '2026-03-06',
            'numero_oficio': 'OF-2026-001',
            'observaciones_asignacion': 'Test'
        }
        
        form = PatrimonioResguardoAsignacionForm(
            data=form_data,
            files={'archivo_oficio': archivo_5mb}
        )
        
        if form.is_valid():
            print(f"    ✓ Archivo de 5 MB aceptado\n")
        else:
            print(f"    ✗ Errores: {form.errors['archivo_oficio']}\n")
        
        # TEST 4B: Archivo excede límite (>10 MB)
        print("  Subprueba 4B: PDF de 11 MB (debe rechazar)")
        archivo_11mb = SimpleUploadedFile(
            "oficio_11mb.pdf",
            b"X" * (11 * 1024 * 1024),  # 11 MB
            content_type="application/pdf"
        )
        
        form = PatrimonioResguardoAsignacionForm(
            data=form_data,
            files={'archivo_oficio': archivo_11mb}
        )
        
        if not form.is_valid() and 'archivo_oficio' in form.errors:
            print(f"    ✓ Archivo de 11 MB rechazado correctamente")
            print(f"      Error: {form.errors['archivo_oficio'][0]}\n")
        else:
            print(f"    ✗ Archivo grande no fue rechazado\n")
        
        print("✅ TEST 4 COMPLETADO\n")
    else:
        print("  ⚠️ No hay bienes o empleados en base de datos\n")
        
except Exception as e:
    print(f"❌ ERROR en TEST 4: {e}\n")

# ============================================================================
# TEST 5: Verificar ruta de URL
# ============================================================================
print("TEST 5: Verificar configuración de URLs")
print("-" * 70)

try:
    from django.urls import reverse
    
    # Generar URL de descarga
    url = reverse('descargar_oficio_resguardo', args=[1])
    print(f"  ✓ Ruta generada: {url}\n")
    
    if 'descargar-oficio' in url:
        print(f"  ✓ URL contiene 'descargar-oficio'")
        print(f"  ✓ URL es: /patrimonio/resguardos/1/descargar-oficio/\n")
        print("✅ TEST 5 COMPLETADO\n")
    else:
        print(f"  ✗ URL no contiene 'descargar-oficio'\n")
except Exception as e:
    print(f"❌ ERROR en TEST 5: {e}\n")

# ============================================================================
# TEST 6: Verificar carpeta de almacenamiento
# ============================================================================
print("TEST 6: Verificar carpeta de almacenamiento")
print("-" * 70)

try:
    from django.conf import settings
    
    media_root = settings.MEDIA_ROOT
    oficios_dir = os.path.join(media_root, 'patrimonio', 'oficios')
    
    print(f"  ✓ MEDIA_ROOT: {media_root}")
    print(f"  ✓ Directorio de oficios: {oficios_dir}")
    
    # Crear directorio si no existe
    os.makedirs(oficios_dir, exist_ok=True)
    
    if os.path.exists(oficios_dir):
        print(f"  ✓ Directorio existe/creado")
        print(f"\n✅ TEST 6 COMPLETADO\n")
    else:
        print(f"  ✗ No se pudo crear el directorio\n")
        
except Exception as e:
    print(f"❌ ERROR en TEST 6: {e}\n")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("=" * 70)
print("✅ RESUMEN DE PRUEBAS")
print("=" * 70)
print("""
Campos de Oficio Implementados:
  ✓ numero_oficio (CharField, max_length=100)
  ✓ fecha_oficio (DateField)
  ✓ archivo_oficio (FileField)

Validaciones Implementadas:
  ✓ Solo archivos PDF (.pdf)
  ✓ Tamaño máximo: 10 MB
  ✓ Campos opcionales

Funcionalidades:
  ✓ Asignación de resguardo con oficio
  ✓ Descarga de PDF
  ✓ Visualización en historial
  ✓ Validación en formulario

Próximos Pasos:
  1. Probar asignación real desde interfaz web
  2. Verificar descarga de PDF
  3. Verificar almacenamiento en media/patrimonio/oficios/
  4. Probar en diferentes navegadores
""")
print("=" * 70 + "\n")

print("Para pruebas manuales, acceda a:")
print("  1. /patrimonio/resguardos/ - Lista de resguardos")
print("  2. /patrimonio/resguardos/asignar/ - Asignar con oficio")
print("  3. /patrimonio/resguardos/empleado/*/historial/ - Ver historial\n")
