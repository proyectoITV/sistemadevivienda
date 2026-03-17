from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0040_vehiculos_area_resguardante'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehiculos',
            name='revisado',
        ),
        migrations.AlterField(
            model_name='vehiculos',
            name='comentario',
            field=models.TextField(blank=True, db_column='Comentario'),
        ),
    ]
