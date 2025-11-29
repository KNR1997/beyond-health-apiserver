from django.db import models

from core.models.base import BaseModel


# Create your models here.
class Treatment(BaseModel):
    CATEGORY_CHOICES = (
        ('preventive', 'Preventive'),
        ('restorative', 'Restorative'),
        ('cosmetic', 'Cosmetic'),
        ('orthodontic', 'Orthodontic'),
        ('surgical', 'Surgical'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    duration = models.IntegerField()  # in minutes
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
