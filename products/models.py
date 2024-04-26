from django.db import models

from accounts.models import UserAccount
from shops.models import Shop


# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)  # Add translated_languages field
    slug = models.CharField(max_length=20, unique=True)
    banners = models.JSONField(default=list)
    promotional_sliders = models.JSONField(default=list)
    settings = models.JSONField(default=dict)
    icon = models.CharField(max_length=20, default='default_icon')
    created_by = models.ForeignKey(UserAccount, related_name='type_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='type_updated', on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.ForeignKey(Type, related_name='type', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, null=True, blank=True)
    image = models.JSONField(default=list)  # Assuming it's a JSON field
    details = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    # translated_languages = models.JSONField(default=["en"])  # New field for translated languages
    translated_languages = models.JSONField(default=list, blank=True)  # Use a callable for default value
    parent = models.ForeignKey('self', related_name='children', null=True, blank=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(UserAccount, related_name='category_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='category_updated', on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def default_translated_languages():
        return ["en"]


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    description = models.TextField()  # Modify to TextField to accommodate longer descriptions
    type = models.ForeignKey(Type, on_delete=models.CASCADE, default=None)  # Add this field
    categories = models.ManyToManyField(Category)  # Many-to-many relationship with Category
    product_type = models.CharField(max_length=20, default='simple')
    language = models.CharField(max_length=10, default='en')
    translated_languages = models.JSONField(default=["en"])  # New field for translated languages
    image = models.JSONField(default=dict)  # Add this field
    gallery = models.JSONField(default=list)  # Add this field
    created_by = models.ForeignKey(UserAccount, related_name='products_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='products_updated', on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=255)
    shop_id = models.IntegerField()  # Assuming shop_id is an integer field
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)
    slug = models.CharField(max_length=255)
    created_by = models.ForeignKey(UserAccount, related_name='attributes_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='attributes_updated', on_delete=models.CASCADE, null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.name


class VariantOption(models.Model):
    attribute = models.ForeignKey(Variant, related_name='variant', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    meta = models.CharField(max_length=255)
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)
    created_by = models.ForeignKey(UserAccount, related_name='variant_option_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='variant_option_updated', on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.value


class ProductVariantOption(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    variant = models.ForeignKey(Variant, related_name='product_variant', on_delete=models.CASCADE)
    variant_option = models.ForeignKey(VariantOption, related_name='product_variant_option', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    min_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, default='publish')  # Add status field with default value
    popular_product = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    in_stock = models.BooleanField(default=True)
    is_taxable = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey(UserAccount, related_name='product_variant_option_created', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(UserAccount, related_name='product_variant_option_updated', on_delete=models.CASCADE,
                                   null=True,
                                   blank=True)
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return f"{self.product.name} - {self.value}"
