# Django imports
from django.db import models

# Module imports
from .base import BaseModel


class Billing(BaseModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(
        'db.Patient', on_delete=models.CASCADE
    )
    appointment = models.ForeignKey(
        'db.Appointment', on_delete=models.SET_NULL, null=True, blank=True
    )
    treatment_plan = models.ForeignKey(
        'db.TreatmentPlan', on_delete=models.SET_NULL, null=True, blank=True
    )
    invoice_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    insurance_covered = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    patient_balance = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "billing"
