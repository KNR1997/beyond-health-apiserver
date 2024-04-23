from decimal import Decimal

from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'min_price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type', 'sku', 'unit', 'translated_languages']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        # data['max_price'] = Decimal(data['max_price'])
        # data['min_price'] = Decimal(data['min_price'])
        return data
