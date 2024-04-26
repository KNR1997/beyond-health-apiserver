from decimal import Decimal

from rest_framework import serializers

from products.models import Product, Type, Category, Variant, VariantOption


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
                  'image', 'gallery', 'product_type', 'translated_languages', 'discount']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        # data['max_price'] = Decimal(data['max_price'])
        # data['min_price'] = Decimal(data['min_price'])
        return data


# class ProductVariationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ProductVariation
#         fields = ['id', 'product', 'attribute', 'value', 'price', 'quantity']
#
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data['price'] = Decimal(data['price'])
#         return data


class ProductDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()  # Nested TypeSerializer
    categories = CategorySerializer(many=True)  # Nested CategorySerializer

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type', 'translated_languages', 'discount', 'categories']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        return data


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'description', 'price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type', 'translated_languages', 'created_by']


class VariantOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    values = VariantOptionsSerializer(many=True, read_only=True)

    class Meta:
        model = Variant
        fields = ['id', 'name', 'shop_id', 'language', 'translated_languages', 'slug', 'values']
