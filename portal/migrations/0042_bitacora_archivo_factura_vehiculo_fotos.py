from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0041_vehiculos_quitar_revisado_comentario_opcional'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculosbitacora',
            name='archivo_factura',
            field=models.FileField(blank=True, db_column='Archivo_factura', null=True, upload_to='vehiculos/facturas/'),
        ),
        migrations.CreateModel(
            name='VehiculoFoto',
            fields=[
                ('idfoto', models.AutoField(primary_key=True, serialize=False)),
                ('imagen', models.ImageField(upload_to='vehiculos/fotos/')),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('fecha_captura', models.DateTimeField(auto_now_add=True)),
                ('vehiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fotos', to='anuncios.vehiculos')),
            ],
            options={
                'verbose_name': 'Foto de Vehiculo',
                'verbose_name_plural': 'Fotos de Vehiculos',
                'db_table': 'vehiculo_fotos',
                'ordering': ['-fecha_captura'],
            },
        ),
    ]
