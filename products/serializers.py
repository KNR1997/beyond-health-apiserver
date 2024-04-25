from decimal import Decimal

from rest_framework import serializers

from products.models import Product, Type, Category


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type', 'sku', 'unit', 'translated_languages', 'discount']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        # data['max_price'] = Decimal(data['max_price'])
        # data['min_price'] = Decimal(data['min_price'])
        return data


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type', 'sku', 'unit', 'translated_languages', 'created_by']
