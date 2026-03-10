# Generated migration for ColaCorreos model

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0017_alter_personalempleados_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='ColaCorreos',
            fields=[
                ('id_cola', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_correo', models.CharField(choices=[('bienvenida', 'Bienvenida con Credenciales'), ('recuperacion', 'Recuperación de Contraseña'), ('credenciales', 'Reenvío de Credenciales'), ('contacto', 'Confirmación de Contacto'), ('otro', 'Otro')], help_text='Tipo de correo', max_length=20)),
                ('email_destino', models.EmailField(help_text='Correo destino', max_length=254)),
                ('asunto', models.CharField(help_text='Asunto del correo', max_length=255)),
                ('contenido_texto', models.TextField(help_text='Contenido en texto plano')),
                ('contenido_html', models.TextField(help_text='Contenido en HTML')),
                ('estado', models.CharField(choices=[('pendiente', 'Pendiente'), ('enviado', 'Enviado Correctamente'), ('error', 'Error')], default='pendiente', help_text='Estado del envío', max_length=20)),
                ('mensaje_error', models.TextField(blank=True, help_text='Mensaje de error si falló el envío')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha de creación del registro')),
                ('fecha_envio', models.DateTimeField(blank=True, null=True, help_text='Fecha cuando se envió correctamente')),
                ('numero_intentos', models.IntegerField(default=0, help_text='Número de intentos de envío')),
                ('id_empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='correos_cola', to='anuncios.personalempleados')),
            ],
            options={
                'verbose_name': 'Cola de Correos',
                'verbose_name_plural': 'Cola de Correos',
                'db_table': 'cola_correos',
            },
        ),
        migrations.AddIndex(
            model_name='colacorreos',
            index=models.Index(fields=['estado', 'fecha_creacion'], name='cola_correos_estado_1234_idx'),
        ),
        migrations.AddIndex(
            model_name='colacorreos',
            index=models.Index(fields=['email_destino'], name='cola_correos_email_5678_idx'),
        ),
    ]
