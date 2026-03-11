# Generated migration for PersonalPuestos model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0011_personalempleados_idtipodecontratacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalPuestos',
            fields=[
                ('idpuesto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre del puesto', max_length=150, unique=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción del puesto')),
                ('activo', models.BooleanField(default=True, help_text='Indica si el puesto está vigente')),
                ('fecha_captura', models.DateTimeField(auto_now_add=True, help_text='Fecha cuando se registró el puesto')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha de la última modificación')),
                ('usuario_captura', models.CharField(blank=True, help_text='Usuario que capturó el registro', max_length=100)),
                ('usuario_modificacion', models.CharField(blank=True, help_text='Usuario que modificó el registro', max_length=100)),
            ],
            options={
                'verbose_name': 'Puesto',
                'verbose_name_plural': 'Puestos',
                'db_table': 'personal_puestos',
            },
        ),
    ]
