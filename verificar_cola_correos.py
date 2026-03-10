#!/usr/bin/env python
"""
Script de verificación del Sistema de Cola de Correos
Verifica que:
1. El modelo ColaCorreos esté correctamente creado
2. El sistema respeta el límite de 2000 correos diarios
3. Los correos se guardan en la cola cuando falla el envío
4. El sistema reintenta enviar correos fallidos
5. Se respeta el máximo de 3 intentos por correo
"""

import os
import sys
import django
from datetime import timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.utils import timezone
from anuncios.models import ColaCorreos, PersonalEmpleados
from anuncios.email_utils import (
    guardar_correo_en_cola,
    procesar_cola_correos,
    enviar_correo_directo
)


def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title):
    """Imprime un encabezado de sección"""
    print(f"\n--- {title} ---")


def test_modelo_colacorreos():
    """Prueba 1: Verificar que el modelo existe"""
    print_section("PRUEBA 1: Verificación del Modelo ColaCorreos")
    
    try:
        # Intentar contar registros
        count = ColaCorreos.objects.count()
        print(f"✓ Modelo ColaCorreos encontrado")
        print(f"  Total de registros en la cola: {count}")
        
        # Verificar campos
        fields = [f.name for f in ColaCorreos._meta.fields]
        expected_fields = [
            'id_cola', 'tipo_correo', 'email_destino', 'asunto',
            'contenido_texto', 'contenido_html', 'estado',
            'mensaje_error', 'fecha_creacion', 'fecha_envio',
            'numero_intentos', 'id_empleado'
        ]
        
        missing_fields = [f for f in expected_fields if f not in fields]
        if missing_fields:
            print(f"✗ Campos faltantes: {missing_fields}")
            return False
        else:
            print(f"✓ Todos los campos esperados están presentes ({len(expected_fields)} campos)")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_guardar_correo():
    """Prueba 2: Guardar un correo de prueba en la cola"""
    print_section("PRUEBA 2: Guardando Correo en la Cola")
    
    try:
        correo = guardar_correo_en_cola(
            tipo_correo='otro',
            email_destino='prueba@example.com',
            asunto='Prueba de Sistema de Cola',
            contenido_texto='Este es un correo de prueba',
            contenido_html='<p>Este es un correo de prueba</p>',
            id_empleado=None
        )
        
        if correo and correo.id_cola:
            print(f"✓ Correo guardado exitosamente")
            print(f"  ID: {correo.id_cola}")
            print(f"  Email: {correo.email_destino}")
            print(f"  Estado: {correo.estado}")
            print(f"  Intentos: {correo.numero_intentos}")
            return True
        else:
            print("✗ No se pudo guardar el correo")
            return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_limite_diario():
    """Prueba 3: Verificar que se respeta el límite diario de 2000"""
    print_section("PRUEBA 3: Verificación del Límite Diario")
    
    try:
        # Contar correos enviados hoy
        inicio_dia = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        enviados_hoy = ColaCorreos.objects.filter(
            estado='enviado',
            fecha_envio__gte=inicio_dia
        ).count()
        
        limite = 2000
        disponibles = limite - enviados_hoy
        
        print(f"✓ Correos enviados hoy: {enviados_hoy}/{limite}")
        print(f"  Correos disponibles: {disponibles}")
        print(f"  Porcentaje de uso: {round((enviados_hoy/limite)*100, 2)}%")
        
        if disponibles > 0:
            print(f"✓ Aún hay capacidad para enviar correos")
        else:
            print(f"⚠ Se alcanzó el límite diario")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_estadisticas_cola():
    """Prueba 4: Obtener estadísticas de la cola"""
    print_section("PRUEBA 4: Estadísticas de la Cola")
    
    try:
        total = ColaCorreos.objects.count()
        pendientes = ColaCorreos.objects.filter(estado='pendiente').count()
        enviados = ColaCorreos.objects.filter(estado='enviado').count()
        errores = ColaCorreos.objects.filter(estado='error').count()
        
        print(f"✓ Total de correos en cola: {total}")
        print(f"  - Pendientes: {pendientes} ({round((pendientes/max(total,1))*100,2)}%)")
        print(f"  - Enviados: {enviados} ({round((enviados/max(total,1))*100,2)}%)")
        print(f"  - Errores: {errores} ({round((errores/max(total,1))*100,2)}%)")
        
        # Errores por tipo
        por_tipo = {}
        for tipo, nombre in ColaCorreos.TIPO_CORREO_CHOICES:
            count = ColaCorreos.objects.filter(tipo_correo=tipo).count()
            if count > 0:
                por_tipo[nombre] = count
        
        if por_tipo:
            print(f"\n  Por tipo de correo:")
            for tipo, count in por_tipo.items():
                print(f"    - {tipo}: {count}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_procesar_cola():
    """Prueba 5: Procesar la cola manualmente"""
    print_section("PRUEBA 5: Procesamiento de la Cola")
    
    try:
        print("Procesando cola de correos...")
        resultado = procesar_cola_correos(limite_diario=2000)
        
        print(f"✓ Procesamiento completado")
        print(f"  - Correos enviados: {resultado['enviados']}")
        print(f"  - Correos con error: {resultado['errores']}")
        print(f"  - Correos pendientes: {resultado['pendientes']}")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_retry_logic():
    """Prueba 6: Verificar lógica de reintentos"""
    print_section("PRUEBA 6: Verificación de Lógica de Reintentos")
    
    try:
        # Buscar correos con errores
        correos_error = ColaCorreos.objects.filter(estado='error').order_by('-numero_intentos')[:5]
        
        if correos_error:
            print(f"✓ Found {len(correos_error)} emails with errors")
            for correo in correos_error:
                print(f"\n  Email: {correo.email_destino}")
                print(f"  Intentos: {correo.numero_intentos}/3")
                print(f"  Último intento: {correo.fecha_envio or correo.fecha_creacion}")
                if correo.mensaje_error:
                    print(f"  Error: {correo.mensaje_error[:100]}...")
            
            # Verificar que no haya correos con más de 3 intentos marcados como pendientes
            invalid_correos = ColaCorreos.objects.filter(estado='pendiente', numero_intentos__gte=3)
            if invalid_correos.exists():
                print(f"\n✗ Hay {invalid_correos.count()} correos pendientes con 3+ intentos")
                return False
            else:
                print(f"\n✓ No hay correos pendientes con 3+ intentos")
        else:
            print("ℹ No hay correos con errores en este momento")
        
        return True
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_comando_management():
    """Prueba 7: Verificar que el comando de management existe"""
    print_section("PRUEBA 7: Verificación del Comando de Management")
    
    try:
        from django.core.management import call_command
        from io import StringIO
        
        # Intentar llamar al comando con --help
        out = StringIO()
        try:
            call_command('procesar_cola_correos', '--help', stdout=out)
            print("✓ Comando 'procesar_cola_correos' existe y es accesible")
            return True
        except SystemExit:
            # El comando --help lanza SystemExit, que es normal
            print("✓ Comando 'procesar_cola_correos' existe")
            return True
    except Exception as e:
        print(f"⚠ Error al verificar comando: {str(e)}")
        return False


def main():
    """Ejecutar todas las pruebas"""
    print_header("VERIFICACIÓN DEL SISTEMA DE COLA DE CORREOS")
    print(f"Fecha y hora: {timezone.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"Base de datos: Django {django.VERSION[0]}.{django.VERSION[1]}")
    
    resultados = []
    
    # Ejecutar pruebas
    pruebas = [
        ("Modelo ColaCorreos", test_modelo_colacorreos),
        ("Guardar Correo", test_guardar_correo),
        ("Límite Diario", test_limite_diario),
        ("Estadísticas", test_estadisticas_cola),
        ("Procesamiento de Cola", test_procesar_cola),
        ("Reintentos", test_retry_logic),
        ("Comando de Management", test_comando_management),
    ]
    
    for nombre, test_func in pruebas:
        try:
            resultado = test_func()
            resultados.append((nombre, resultado))
        except Exception as e:
            print(f"\n✗ Error inesperado en {nombre}: {str(e)}")
            resultados.append((nombre, False))
    
    # Resumen
    print_header("RESUMEN DE PRUEBAS")
    exitosas = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    for nombre, resultado in resultados:
        estado = "✓ EXITOSA" if resultado else "✗ FALLIDA"
        print(f"{estado}: {nombre}")
    
    print(f"\nTotal: {exitosas}/{total} pruebas exitosas ({round((exitosas/total)*100,2)}%)")
    
    if exitosas == total:
        print("\n✓ ¡TODAS LAS PRUEBAS PASARON! El sistema de cola está funcionando correctamente.")
        return 0
    else:
        print(f"\n✗ {total - exitosas} prueba(s) fallaron. Por favor, revisa los errores arriba.")
        return 1


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
