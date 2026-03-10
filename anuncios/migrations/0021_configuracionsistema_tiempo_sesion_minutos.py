# Generated migration for ConfiguracionSistema - Agregar campo tiempo_sesion_minutos

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0020_merge_20260306_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuracionsistema',
            name='tiempo_sesion_minutos',
            field=models.IntegerField(
                default=15,
                help_text='Tiempo de inactividad en minutos para cerrar la sesión (default: 15 minutos)'
            ),
        ),
    ]
