from django.db import models

from authentication.models import User
from core.models.base import BaseModel


# Create your models here.
class ClinicSettings(BaseModel):
    clinic_name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    working_hours = models.JSONField()  # Store working hours as JSON
    appointment_duration = models.IntegerField(default=30)  # default duration in minutes
    cancellation_notice_hours = models.IntegerField(default=24)


class Notification(models.Model):
    TYPE_CHOICES = (
        ('appointment_reminder', 'Appointment Reminder'),
        ('billing', 'Billing'),
        ('system', 'System Notification'),
        ('announcement', 'Announcement'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_object_id = models.IntegerField(null=True, blank=True)  # Generic foreign key
