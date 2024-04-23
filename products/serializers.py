from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'min_price', 'max_price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type']
