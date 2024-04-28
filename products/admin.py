from django.contrib import admin

from products.models import Type, Category, BaseProduct, Variant, VariantOption, BaseProductVariant, \
    BaseProductVariantOption, Product, ProductStock

# Register your models here.
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(BaseProduct)
admin.site.register(Variant)
admin.site.register(VariantOption)
admin.site.register(BaseProductVariant)
admin.site.register(BaseProductVariantOption)
admin.site.register(Product)
admin.site.register(ProductStock)
