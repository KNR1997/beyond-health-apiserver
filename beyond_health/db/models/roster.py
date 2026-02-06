from django.db import models
from rest_framework.exceptions import ValidationError

from beyond_health.db.models.base import BaseModel


class RosterWeek(BaseModel):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('PUBLISHED', 'Published'),
        ('LOCKED', 'Locked'),
    )

    week_start_date = models.DateField(unique=True)
    week_end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='DRAFT')

    def __str__(self):
        return f"Roster {self.week_start_date}"


class RosterAssignment(models.Model):
    ROLE_REQUIRED = (
        ('DENTIST', 'Dentist'),
        ('SUPPORT', 'Support'),
    )

    roster_week = models.ForeignKey(
        RosterWeek, on_delete=models.CASCADE, related_name='assignments'
    )
    date = models.DateField()
    shift = models.ForeignKey('db.Shift', on_delete=models.PROTECT)
    user = models.ForeignKey('db.User', on_delete=models.PROTECT)
    assigned_role = models.CharField(max_length=10, choices=ROLE_REQUIRED)

    class Meta:
        unique_together = ('date', 'shift', 'user')
        indexes = [
            models.Index(fields=['roster_week']),
            models.Index(fields=['date', 'shift']),
        ]

    def clean(self):
        """
        Business rule validation
        """
        if self.assigned_role != self.user.role:
            raise ValidationError("Assigned role does not match user role")

    def __str__(self):
        return f"{self.date} - {self.shift} - {self.user}"
