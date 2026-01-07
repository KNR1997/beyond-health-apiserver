# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class PatientDentalProblem(BaseModel):
    class Severity(models.TextChoices):
        MILD = 'mild', 'Mild'
        MODERATE = 'moderate', 'Moderate'
        SEVERE = 'severe', 'Severe'

    patient = models.ForeignKey(
        'db.Patient', on_delete=models.CASCADE, related_name='patient_problems'
    )
    dental_problem = models.ForeignKey(
        'db.DentalProblem', on_delete=models.CASCADE, related_name='patient_problems'
    )
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MODERATE)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('patient', 'dental_problem')
