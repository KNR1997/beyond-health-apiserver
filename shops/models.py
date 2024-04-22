from django.db import models


# Create your models here.


class Shop(models.Model):
    owner_id = models.IntegerField()  # Assuming owner_id is an integer field
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)  # Allow null and blank
    cover_image_thumbnail = models.URLField()  # Assuming thumbnail is a URL
    cover_image_original = models.URLField()  # Assuming original is a URL
    logo_thumbnail = models.URLField()  # Assuming thumbnail is a URL
    logo_original = models.URLField()  # Assuming original is a URL
    is_active = models.BooleanField(default=True)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.CharField(max_length=20)
    street_address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20, blank=True, null=True)  # Allow null and blank
    website = models.URLField(blank=True, null=True)  # Allow null and blank
    orders_count = models.IntegerField(default=0)  # Assuming orders_count is an integer
    products_count = models.IntegerField(default=0)  # Assuming products_count is an integer
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return self.name
