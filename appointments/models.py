from django.db import models

from core.models.base import BaseModel
from user.models import Patient, Dentist


# Create your models here.
class Appointment(BaseModel):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    duration = models.IntegerField(default=30)  # in minutes
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    appointment_type = models.CharField(max_length=100)  # e.g., 'Checkup', 'Cleaning', 'Filling'
    reason_for_visit = models.TextField(blank=True)
    notes = models.TextField(blank=True)