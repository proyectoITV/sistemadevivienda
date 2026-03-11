# Generated migration to split nombre_completo into three fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0013_personalempleados_idpuesto'),
    ]

    operations = [
        migrations.AddField(
            model_name='personalempleados',
            name='apellido_materno',
            field=models.CharField(blank=True, help_text='Apellido materno del empleado', max_length=100),
        ),
        migrations.AddField(
            model_name='personalempleados',
            name='apellido_paterno',
            field=models.CharField(help_text='Apellido paterno del empleado', max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='personalempleados',
            name='nombre',
            field=models.CharField(help_text='Nombre(s) del empleado', max_length=100, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='personalempleados',
            name='nombre_completo',
            field=models.CharField(editable=False, help_text='Se genera automáticamente', max_length=200),
        ),
    ]
