from django.apps import AppConfig


from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.core.management import call_command
from django.conf import settings
import os

class PortalConfig(AppConfig):
    name = 'portal'
    label = 'anuncios'

    def ready(self):
        from portal.models import PersonalEmpleados
        def crear_usuario_demo_signal(sender, **kwargs):
            if PersonalEmpleados.objects.count() == 0:
                # Ejecutar el script solo si no hay empleados
                script_path = os.path.join(settings.BASE_DIR, 'crear_usuario_demo.py')
                if os.path.exists(script_path):
                    # Ejecutar el script como un subproceso
                    import subprocess, sys
                    subprocess.run([sys.executable, script_path], check=False)

        post_migrate.connect(crear_usuario_demo_signal, sender=self)
