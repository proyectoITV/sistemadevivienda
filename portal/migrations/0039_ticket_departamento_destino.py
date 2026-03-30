from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def poblar_departamento_desde_receptor(apps, schema_editor):
    TicketServicio = apps.get_model('anuncios', 'TicketServicio')

    for ticket in TicketServicio.objects.select_related('receptor').all():
        if ticket.departamento_destino_id:
            continue

        receptor = getattr(ticket, 'receptor', None)
        departamento_id = getattr(receptor, 'iddepartamento_id', None) if receptor else None

        if departamento_id:
            ticket.departamento_destino_id = departamento_id
            ticket.save(update_fields=['departamento_destino'])


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0038_tickets_servicio'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketservicio',
            name='atendido_por',
            field=models.ForeignKey(blank=True, help_text='Empleado del departamento que toma el ticket', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets_atendidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ticketservicio',
            name='departamento_destino',
            field=models.ForeignKey(blank=True, help_text='Departamento destino del ticket', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tickets_recibidos_departamento', to='anuncios.personaldepartamento'),
        ),
        migrations.AlterField(
            model_name='ticketservicio',
            name='receptor',
            field=models.ForeignKey(blank=True, help_text='A quien va dirigido el ticket', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='tickets_recibidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(poblar_departamento_desde_receptor, migrations.RunPython.noop),
        migrations.RemoveIndex(
            model_name='ticketservicio',
            name='tickets_ser_emisor__83a222_idx',
        ),
        migrations.AddIndex(
            model_name='ticketservicio',
            index=models.Index(fields=['emisor', 'departamento_destino'], name='tickets_ser_emisor__dep_idx'),
        ),
    ]
