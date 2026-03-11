# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0016_configuracionsistema_usuariosdelsistema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalempleados',
            name='usuario',
            field=models.CharField(blank=True, help_text='Nombre de usuario para login', max_length=100, null=True, unique=True),
        ),
    ]
