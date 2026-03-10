# Generated migration for PersonalTipoDeContratacion model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0009_personalempleados_fotografia'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalTipoDeContratacion',
            fields=[
                ('idtipodecontratacion', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(help_text='Nombre del tipo de contratación', max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, help_text='Descripción del tipo de contratación')),
                ('activo', models.BooleanField(default=True, help_text='Indica si el tipo de contratación está vigente')),
                ('fecha_captura', models.DateTimeField(auto_now_add=True, help_text='Fecha cuando se registró el tipo')),
                ('fecha_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha de la última modificación')),
                ('usuario_captura', models.CharField(blank=True, help_text='Usuario que capturó el registro', max_length=100)),
                ('usuario_modificacion', models.CharField(blank=True, help_text='Usuario que modificó el registro', max_length=100)),
            ],
            options={
                'verbose_name': 'Tipo de Contratación',
                'verbose_name_plural': 'Tipos de Contratación',
                'db_table': 'personal_tipodecontratacion',
            },
        ),
    ]
