from datetime import timedelta

from django.db import migrations


def backfill_sla_tickets_mantenimiento(apps, schema_editor):
    TicketMantenimiento = apps.get_model('anuncios', 'TicketMantenimiento')

    sla_por_prioridad = {
        'baja': 72,
        'normal': 48,
        'alta': 24,
        'critica': 8,
    }

    qs = TicketMantenimiento.objects.filter(fecha_limite_sla__isnull=True)

    for ticket in qs.iterator():
        sla_horas = sla_por_prioridad.get(ticket.prioridad, 48)
        fecha_base = ticket.fecha_creacion
        if fecha_base is None:
            continue

        ticket.sla_horas_objetivo = sla_horas
        ticket.fecha_limite_sla = fecha_base + timedelta(hours=sla_horas)
        ticket.save(update_fields=['sla_horas_objetivo', 'fecha_limite_sla'])


def reverse_backfill_sla_tickets_mantenimiento(apps, schema_editor):
    # No-op intencional para no borrar datos de SLA una vez calculados.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('anuncios', '0043_ticketmantenimiento_fecha_limite_sla_and_more'),
    ]

    operations = [
        migrations.RunPython(
            backfill_sla_tickets_mantenimiento,
            reverse_backfill_sla_tickets_mantenimiento,
        ),
    ]
