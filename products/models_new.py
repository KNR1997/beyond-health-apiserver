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
    created_by = models.ForeignKey(
        UserAccount,
        related_name='types_created',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(
        UserAccount,
        related_name='types_updated',
        on_delete=models.CASCADE, null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    type = models.ForeignKey(
        Type,
        related_name='categories',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    icon = models.CharField(max_length=255, null=True, blank=True)
    image = models.JSONField(default=list)  # Assuming it's a JSON field
    details = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en')
    # translated_languages = models.JSONField(default=["en"])  # New field for translated languages
    translated_languages = models.JSONField(default=list, blank=True)  # Use a callable for default value
    parent = models.ForeignKey(
        'self',
        related_name='children',
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        UserAccount,
        related_name='categories_created',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(
        UserAccount,
        related_name='categories_updated',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @staticmethod
    def default_translated_languages():
        return ["en"]


class BaseProduct(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    description = models.TextField()  # Modify to TextField to accommodate longer descriptions
    type = models.ForeignKey(Type, on_delete=models.CASCADE, default=None)  # Add this field
    categories = models.ManyToManyField(
        Category,
        related_name='base_products'
    )
    product_type = models.CharField(max_length=20, default='simple')
    quantity = models.IntegerField(default=1)
    price = models.FloatField(null=True)
    min_price = models.FloatField(null=True)
    max_price = models.FloatField(null=True)
    language = models.CharField(max_length=10, default='en')
    translated_languages = models.JSONField(default=["en"])  # New field for translated languages
    image = models.JSONField(default=dict)  # Add this field
    gallery = models.JSONField(default=list)  # Add this field
    tags = models.JSONField(default=list)  # Add this field
    status = models.CharField(max_length=20, default='publish')  # Add status field with default value
    created_by = models.ForeignKey(
        UserAccount,
        related_name='products_created',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(
        UserAccount,
        related_name='products_updated',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.name


class Variant(models.Model):
    name = models.CharField(max_length=255)
    shop_id = models.IntegerField()  # Assuming shop_id is an integer field
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)
    slug = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        UserAccount,
        related_name='created_variants',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(
        UserAccount,
        related_name='updated_variants',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.name


class VariantOption(models.Model):
    variant = models.ForeignKey(
        Variant,
        related_name='variant_options',
        on_delete=models.CASCADE
    )
    variant_name = models.CharField(max_length=255)
    variant_option_name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    meta = models.CharField(max_length=255)
    language = models.CharField(max_length=10)
    translated_languages = models.JSONField(default=list)
    first_letters = models.CharField(max_length=3, blank=True)  # New field for storing first letters
    created_by = models.ForeignKey(
        UserAccount,
        related_name='created_variant_options',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(
        UserAccount,
        related_name='updated_variant_options',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved

    def __str__(self):
        return self.variant_option_name


class BaseProductVariant(models.Model):
    base_product = models.ForeignKey(
        BaseProduct,
        related_name='variants',
        on_delete=models.CASCADE
    )
    base_product_name = models.CharField(max_length=255)
    variant = models.ForeignKey(
        Variant,
        related_name='base_product_variants',
        on_delete=models.CASCADE
    )
    variant_name = models.CharField(max_length=255)


class BaseProductVariantOption(models.Model):
    base_product = models.ForeignKey(
        BaseProduct,
        related_name='variant_options',
        on_delete=models.CASCADE
    )
    base_product_variant = models.ForeignKey(
        BaseProductVariant,
        related_name='variant_options',
        on_delete=models.CASCADE
    )
    variant_option = models.ForeignKey(
        VariantOption,
        related_name='base_product_variant_options',
        on_delete=models.CASCADE
    )
    product_name = models.CharField(max_length=255)
    variant_name = models.CharField(max_length=255)
    variant_option_name = models.CharField(max_length=255)


class Product(models.Model):
    product = models.ForeignKey(
        BaseProduct,
        related_name='products',
        on_delete=models.CASCADE
    )
    combination_string = models.CharField(max_length=255)
    product_type = models.CharField(max_length=20, default='simple')
    sku = models.CharField(max_length=255)
    title = models.CharField(max_length=155, default='Default Title')
    price = models.FloatField()
    sale_price = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    quantity = models.IntegerField()
    in_stock = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='publish')  # Add status field with default value
    popular_product = models.BooleanField(default=False)
    # available_stock = models.IntegerField()
    created_by = models.ForeignKey(
        UserAccount,
        related_name='created_products',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when a new object is created
    updated_by = models.ForeignKey(
        UserAccount,
        related_name='updated_products',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set whenever the object is saved


class ProductStock(models.Model):
    productCombination = models.ForeignKey(
        Product,
        related_name='product_stocks',
        on_delete=models.CASCADE
    )
    total_stock = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
