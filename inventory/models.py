from django.db import models

from core.models.base import BaseModel


# Create your models here.
class Inventory(BaseModel):
    item_name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    minimum_stock = models.IntegerField(default=5)
    unit_cost = models.DecimalField(max_digits=8, decimal_places=2)
    supplier = models.CharField(max_length=100, blank=True)
    last_restocked = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
