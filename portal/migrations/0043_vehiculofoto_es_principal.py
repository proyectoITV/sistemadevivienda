from django.db import migrations, models


def asignar_foto_principal(apps, schema_editor):
    VehiculoFoto = apps.get_model('anuncios', 'VehiculoFoto')
    vehiculos_ids = VehiculoFoto.objects.values_list('vehiculo_id', flat=True).distinct()

    for vehiculo_id in vehiculos_ids:
        fotos = VehiculoFoto.objects.filter(vehiculo_id=vehiculo_id).order_by('-fecha_captura')
        if fotos.exists() and not fotos.filter(es_principal=True).exists():
            foto = fotos.first()
            foto.es_principal = True
            foto.save(update_fields=['es_principal'])


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0042_bitacora_archivo_factura_vehiculo_fotos'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculofoto',
            name='es_principal',
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(asignar_foto_principal, migrations.RunPython.noop),
    ]
