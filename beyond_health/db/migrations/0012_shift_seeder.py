from django.db import migrations
import datetime


def seed_shifts(apps, schema_editor):
    Shift = apps.get_model('db', 'Shift')

    Shift.objects.update_or_create(
        code='MORNING',
        defaults={
            'start_time': datetime.time(6, 0),
            'end_time': datetime.time(14, 0),
            'order_index': 1,
        }
    )

    Shift.objects.update_or_create(
        code='EVENING',
        defaults={
            'start_time': datetime.time(14, 0),
            'end_time': datetime.time(22, 0),
            'order_index': 2,
        }
    )

    Shift.objects.update_or_create(
        code='NIGHT',
        defaults={
            'start_time': datetime.time(22, 0),
            'end_time': datetime.time(6, 0),
            'order_index': 3,
        }
    )


class Migration(migrations.Migration):
    dependencies = [
        ('db', '0011_appointment_appointment_no_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_shifts),
    ]
