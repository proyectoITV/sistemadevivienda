from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0039_vehiculos_catalogos_y_bitacora'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculos',
            name='idareaadscripcion',
            field=models.ForeignKey(blank=True, db_column='IdAreaAdscripcion', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.personaldepartamento'),
        ),
        migrations.AddField(
            model_name='vehiculos',
            name='idresguradante',
            field=models.ForeignKey(blank=True, db_column='IdResguradante', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.personalempleados'),
        ),
    ]
