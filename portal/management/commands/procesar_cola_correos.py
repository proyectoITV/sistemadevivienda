from django.core.management.base import BaseCommand
from portal.email_utils import procesar_cola_correos


class Command(BaseCommand):
    help = 'Procesa la cola de correos pendientes de envío'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limite',
            type=int,
            default=2000,
            help='Límite de correos a enviar en este proceso (default: 2000)',
        )

    def handle(self, *args, **options):
        limite = options['limite']
        
        self.stdout.write(
            self.style.WARNING(f'🚀 Iniciando procesamiento de cola de correos (límite: {limite})...')
        )
        
        resultado = procesar_cola_correos(limite_diario=limite)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✓ Procesamiento completado:\n'
                f'  - Enviados: {resultado["enviados"]}\n'
                f'  - Errores: {resultado["errores"]}\n'
                f'  - Pendientes: {resultado["pendientes"]}'
            )
        )
