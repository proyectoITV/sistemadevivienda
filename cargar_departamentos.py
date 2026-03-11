import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.models import PersonalDepartamento, PersonalDireccion

# Datos de departamentos a cargar
DEPARTAMENTOS = [
    (1, 'DIRECCION GENERAL', 1),
    (2, 'SECRETARIA PARTICULAR', 1),
    (3, 'ATENCION CUIDADANA', 1),
    (4, 'DEPARTAMENTO DE CONTROL DOCUMENTAL', 1),
    (5, 'DEPARTAMENTO DE SOPORTE TECNICO', 1),
    (57, 'DEPARTAMENTO DE INFORMATICA', 1),
    (6, 'DIRECCION DE PLANEACION Y EVALUACION', 3),
    (7, 'DEPARTAMENTO DE EVALUACION DE PROYECTOS', 3),
    (8, 'DEPARTAMENTO DE INDICADORES DE VIVIENDA', 3),
    (9, 'DEPARTAMENTO DE SISTEMAS DE INFORMACION GEOGRAFIA', 3),
    (10, 'DIRECCION JURIDICA Y SEGURIDAD PATRIMONIAL', 4),
    (11, 'SUBDIRECCION DE ESCRITURACION', 4),
    (12, 'DEPARTAMENTO DE VINCULACION CON EL SISTEMA REGISTRAL Y CATASTRAL', 4),
    (13, 'DEPARTAMENTO DE CONTROL Y CAPTURA', 4),
    (14, 'SUBDIRECCION DE ASUNTOS LEGALES', 4),
    (15, 'DEPARTAMENTO DE ATENCION A JUICIOS', 4),
    (16, 'DEPARTAMENTO DE LO JURIDICO ADMINISTRATIVO', 4),
    (17, 'SUBDIRECCION DE REGULARIZACION', 4),
    (18, 'DEPARTAMENTO DE APOYO A ASUNTOS DE REGULARIZACION', 4),
    (19, 'COORDINACION DE DELEGACIONES', 2),
    (20, 'DELEGACION ABASOLO', 2),
    (21, 'DELEGACION ALDAMA', 2),
    (22, 'DELEGACION ALTAMIRA', 2),
    (23, 'DELEGACION CAMARGO', 2),
    (24, 'DELEGACION DIAZ ORDAZ', 2),
    (25, 'DELEGACION GONZALEZ', 2),
    (26, 'DELEGACION JIMENEZ', 2),
    (27, 'DELEGACION LLERA', 2),
    (28, 'DELEGACION MADERO', 2),
    (29, 'DELEGACION MANTE', 2),
    (30, 'DELEGACION MATAMOROS', 2),
    (31, 'DELEGACION NUEVO LAREDO', 2),
    (32, 'DELEGACION MIGUEL ALEMAN', 2),
    (33, 'DELEGACION REYNOSA', 2),
    (34, 'DELEGACION RIO BRAVO', 2),
    (35, 'DELEGACION SAN FERNANDO', 2),
    (36, 'DELEGACION SOTO LA MARINA', 2),
    (37, 'DELEGACION TAMPICO', 2),
    (38, 'DELEGACION TULA', 2),
    (39, 'DELEGACION VALLE HERMOSO', 2),
    (40, 'DELEGACION VILLA DE CASAS', 2),
    (41, 'DELEGACION VICTORIA', 2),
    (42, 'DELEGACION XICOTENCATL', 2),
    (60, 'DEPARTAMENTO DE ENLACE OPERATIVO CON DELEGACIONES MUNICIPALES', 2),
    (61, 'DEPARTAMENTO DE APOYO Y SEGUIMIENTO', 2),
    (62, 'DEPARTAMENTO DE PROGRAMAS DE MEJORAMIENTO DE VIVIENDA', 5),
    (43, 'DIRECCION DE PROGRAMAS DE SUELO Y VIVIENDA', 5),
    (44, 'DEPARTAMENTO DE CONTROL Y SEGUIMIENTO DE PROGRAMAS', 5),
    (45, 'SUBDIRECCION DE PROGRAMAS DE SUELO', 5),
    (46, 'DEPARTAMENTO DE ESTUDIOS Y PROYECTOS', 5),
    (47, 'DEPARTAMENTO DE CONTROL Y SEGUIMIENTO DE PROGRAMAS', 5),
    (48, 'DEPARTAMENTO DE PROGRAMAS DE OFERTA DE SUELO', 5),
    (49, 'SUBDIRECCION DE PROGRAMAS DE VIVIENDA', 5),
    (50, 'DEPARTAMENTO DE PROGRAMAS DE VIVIENDA', 5),
    (51, 'DEPARTAMENTO DE TECNOLOGIAS PARA LA VIVIENDA', 5),
    (52, 'DIRECCION DE ADMINISTRACION Y FINANZAS', 6),
    (53, 'DEPARTAMENTO DE RECURSOS MATERIALES Y SERVICIOS GENERALES', 6),
    (54, 'DEPARTAMENTO DE ADQUISICIONES', 6),
    (55, 'DEPARTAMENTO DE CREDITO', 6),
    (56, 'DEPARTAMENTO DE RECURSOS FINANCIEROS Y GESTION DE RECURSOS', 6),
    (58, 'DEPARTAMENTO DE CONTABILIDAD', 6),
    (59, 'DEPARTAMENTO DE RECURSOS HUMANOS Y PATRIMONIO', 6),
]

def cargar_departamentos():
    """Carga los departamentos iniciales en la tabla personal_departamento"""
    
    departamentos_cargados = 0
    departamentos_existentes = 0
    errores = 0
    
    for iddep, nombre_dep, id_dir in DEPARTAMENTOS:
        try:
            # Verificar que la dirección existe
            direccion = PersonalDireccion.objects.get(iddireccion=id_dir)
            
            obj, creado = PersonalDepartamento.objects.get_or_create(
                iddepartamento=iddep,
                defaults={
                    'departamento': nombre_dep,
                    'iddireccion': direccion,
                    'activo': True,
                    'usuario_captura': 'SISTEMA',
                    'usuario_modificacion': 'SISTEMA',
                }
            )
            
            if creado:
                print(f"✓ Departamento creado: {iddep:2d} - {nombre_dep:60s} → Dirección {id_dir}")
                departamentos_cargados += 1
            else:
                print(f"• Departamento ya existe: {iddep:2d} - {nombre_dep:60s}")
                departamentos_existentes += 1
                
        except PersonalDireccion.DoesNotExist:
            print(f"✗ ERROR: Dirección {id_dir} no existe para el departamento {nombre_dep}")
            errores += 1
        except Exception as e:
            print(f"✗ ERROR al crear {nombre_dep}: {str(e)}")
            errores += 1
    
    print(f"\n{'='*80}")
    print(f"Resumen de carga:")
    print(f"  Departamentos nuevos cargados: {departamentos_cargados}")
    print(f"  Departamentos que ya existían: {departamentos_existentes}")
    print(f"  Errores: {errores}")
    print(f"  Total de departamentos en la BD: {PersonalDepartamento.objects.count()}")
    print(f"{'='*80}")

if __name__ == '__main__':
    cargar_departamentos()
