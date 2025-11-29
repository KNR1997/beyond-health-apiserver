from django.db import models

from appointments.models import Appointment
from core.models.base import BaseModel
from treatments.models import Treatment
from user.models import Patient, Dentist


# Create your models here.
class MedicalRecord(BaseModel):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    diagnosis = models.TextField(blank=True)
    treatment_notes = models.TextField(blank=True)
    prescriptions = models.TextField(blank=True)
    xray_images = models.TextField(blank=True)  # JSON field for image paths
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class TreatmentPlan(BaseModel):
    STATUS_CHOICES = (
        ('proposed', 'Proposed'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    dentist = models.ForeignKey(Dentist, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class TreatmentPlanItem(BaseModel):
    treatment_plan = models.ForeignKey(TreatmentPlan, on_delete=models.CASCADE, related_name='items')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cost = models.DecimalField(max_digits=8, decimal_places=2)
    notes = models.TextField(blank=True)
    tooth_number = models.CharField(max_length=10, blank=True)  # FDI notation
