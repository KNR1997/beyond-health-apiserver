from django.contrib import admin

from products.models import Type, Category, Product, Variant, VariantOption, ProductVariantOption

# Register your models here.
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Variant)
admin.site.register(VariantOption)
admin.site.register(ProductVariantOption)
