# Generated migration to update PersonalEmpleados puesto field

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0012_personalpuestos'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='personalempleados',
            name='puesto',
        ),
        migrations.AddField(
            model_name='personalempleados',
            name='idpuesto',
            field=models.ForeignKey(blank=True, help_text='Puesto del empleado', null=True, on_delete=django.db.models.deletion.SET_NULL, to='anuncios.personalpuestos'),
        ),
    ]
