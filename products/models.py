from django.db import models

from accounts.models import UserAccount
from shops.models import Shop


# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)  # Add translated_languages field
    slug = models.CharField(max_length=20)
    banners = models.JSONField(default=list)
    promotional_sliders = models.JSONField(default=list)
    settings = models.JSONField(default=dict)
    icon = models.CharField(max_length=20, default='default_icon')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default='default-slug')  # Add this field
    description = models.TextField()  # Modify to TextField to accommodate longer descriptions
    type = models.ForeignKey(Type, on_delete=models.CASCADE, default=None)  # Add this field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # shop = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)  # Add this field
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)  # New field for translated languages
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50)  # unidentified attribute
    quantity = models.PositiveIntegerField()
    in_stock = models.BooleanField(default=True)
    is_taxable = models.BooleanField(default=False)
    # shipping class foreignKey
    status = models.CharField(max_length=20, default='publish')  # Add status field with default value
    product_type = models.CharField(max_length=20, default='simple')
    unit = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.JSONField(default=dict)  # Add this field
    gallery = models.JSONField(default=list)  # Add this field
    popular_product = models.BooleanField(default=False)
    created_by = models.ForeignKey(UserAccount, related_name='products_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='products_updated', on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.name
