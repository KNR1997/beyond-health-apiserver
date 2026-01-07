# Django imports
from django.db import models

# Module imports
from .base import BaseModel


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

    user = models.OneToOneField(
        'db.User', on_delete=models.SET_NULL, null=True
    )
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    years_of_experience = models.IntegerField(default=0)
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "dentist"
