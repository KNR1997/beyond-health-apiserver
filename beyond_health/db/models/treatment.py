# Django imports
from django.db import models

# Module imports
from .base import BaseModel


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

    class Meta:
        db_table = "treatment"


class TreatmentPlan(BaseModel):
    STATUS_CHOICES = (
        ('proposed', 'Proposed'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(
        'db.Patient', on_delete=models.CASCADE
    )
    dentist = models.ForeignKey(
        'db.Dentist', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "treatment_plan"


class TreatmentPlanItem(BaseModel):
    treatment_plan = models.ForeignKey(
        'db.TreatmentPlan', on_delete=models.CASCADE, related_name='items'
    )
    treatment = models.ForeignKey(
        'db.Treatment', on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)
    tooth_number = models.CharField(max_length=10, blank=True)  # FDI notation

    class Meta:
        db_table = "patient_plan_item"
