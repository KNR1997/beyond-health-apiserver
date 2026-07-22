# Django imports
from django.db import models
from django.utils import timezone

# Module imports
from .base import BaseModel


class Appointment(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    appointment_no = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
    )
    patient = models.ForeignKey(
        'db.Patient', on_delete=models.CASCADE
    )
    dentist = models.ForeignKey(
        'db.Dentist', on_delete=models.CASCADE, null=True
    )
    appointment_date = models.DateTimeField()
    duration = models.IntegerField(default=30)  # in minutes
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='scheduled')
    # e.g., 'Checkup', 'Cleaning', 'Filling'
    appointment_type = models.CharField(max_length=100)
    reason_for_visit = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        db_table = "appointment"

    def save(self, *args, **kwargs):
        if not self.appointment_no:
            self.appointment_no = self.generate_appointment_no()

        super().save(*args, **kwargs)

    @classmethod
    def generate_appointment_no(cls):
        today = timezone.localdate()
        prefix = f"APT-{today:%Y%m%d}"

        last = (
            cls.objects
            .filter(appointment_no__startswith=prefix)
            .order_by("-appointment_no")
            .first()
        )

        if last:
            sequence = int(last.appointment_no.split("-")[-1]) + 1
        else:
            sequence = 1

        return f"{prefix}-{sequence:04d}"
