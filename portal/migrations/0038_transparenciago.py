from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0037_patrimoniobienesdelinstituto_numinv_monitor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransparenciaGo',
            fields=[
                ('id_file', models.AutoField(db_column='IdFile', primary_key=True, serialize=True)),
                ('file_nombre', models.CharField(db_column='FileNombre', max_length=255, help_text='Nombre del archivo original')),
                ('id_user', models.CharField(db_column='IdUser', max_length=255, help_text='Usuario que subio el archivo')),
                ('fecha', models.DateField(db_column='fecha')),
                ('hora', models.TimeField(db_column='hora')),
                ('file_descripcion', models.TextField(blank=True, db_column='FileDescripcion', help_text='Descripcion del archivo')),
            ],
            options={
                'verbose_name': 'Archivo de Transparencia',
                'verbose_name_plural': 'Archivos de Transparencia',
                'db_table': 'TransparenciaGo',
                'ordering': ['fecha', 'hora', 'id_file'],
            },
        ),
    ]
