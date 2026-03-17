from django.db import migrations, models


def inicializar_orden_fotos(apps, schema_editor):
    VehiculoFoto = apps.get_model('anuncios', 'VehiculoFoto')
    vehiculos_ids = VehiculoFoto.objects.values_list('vehiculo_id', flat=True).distinct()

    for vehiculo_id in vehiculos_ids:
        fotos = VehiculoFoto.objects.filter(vehiculo_id=vehiculo_id).order_by('-es_principal', '-fecha_captura')
        orden = 1
        for foto in fotos:
            foto.orden = orden
            foto.save(update_fields=['orden'])
            orden += 1


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0043_vehiculofoto_es_principal'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculofoto',
            name='orden',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.RunPython(inicializar_orden_fotos, migrations.RunPython.noop),
    ]
