# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Patient(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, null=True, blank=True)
    mobile_number = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_id = models.CharField(max_length=50, blank=True)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    user = models.OneToOneField(
        'db.User', on_delete=models.SET_NULL, null=True
    )
    primary_dentist = models.ForeignKey(
        'db.Dentist', on_delete=models.SET_NULL, null=True
    )

    class Meta:
        db_table = "patient"
