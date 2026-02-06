from django.db import models


class Shift(models.Model):
    SHIFT_CODES = (
        ('MORNING', 'Morning'),
        ('EVENING', 'Evening'),
        ('NIGHT', 'Night'),
    )

    code = models.CharField(max_length=10, choices=SHIFT_CODES, unique=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    order_index = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"{self.code} ({self.start_time}-{self.end_time})"
