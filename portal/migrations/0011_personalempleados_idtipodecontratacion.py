# Generated migration to update PersonalEmpleados tipo_contrato field

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0010_personaltipodecontratacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalempleados',
            name='tipo_contrato',
        ),
        migrations.AddField(
            model_name='personalempleados',
            name='idtipodecontratacion',
            field=models.ForeignKey(blank=True, help_text='Tipo de contratación del empleado', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.personaltipodecontratacion'),
        ),
    ]
