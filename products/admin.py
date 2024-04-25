from django.contrib import admin

from products.models import Type, Category, Product

# Register your models here.
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Product)
