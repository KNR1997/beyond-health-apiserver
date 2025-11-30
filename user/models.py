from django.db import models

from authentication.models import User
from core.models.base import BaseModel


# Create your models here.
class Patient(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    insurance_id = models.CharField(max_length=50, blank=True)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    primary_dentist = models.ForeignKey('Dentist', on_delete=models.SET_NULL, null=True, blank=True)


class Dentist(BaseModel):
    SPECIALIZATION_CHOICES = (
        ('general', 'General Dentistry'),
        ('ortho', 'Orthodontics'),
        ('perio', 'Periodontics'),
        ('endo', 'Endodontics'),
        ('pedo', 'Pedodontics'),
        ('oral_surgery', 'Oral Surgery'),
        ('prostho', 'Prosthodontics'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True) # todo -> missing unique
    years_of_experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)


class Staff(BaseModel):
    ROLE_CHOICES = (
        ('receptionist', 'Receptionist'),
        ('assistant', 'Dental Assistant'),
        ('hygienist', 'Dental Hygienist'),
        ('manager', 'Office Manager'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
