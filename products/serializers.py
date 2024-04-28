from decimal import Decimal

from rest_framework import serializers

from products.models import BaseProduct, Type, Category, Variant, Product, BaseProductVariant, \
    BaseProductVariantOption


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class ProductDetailSerializer(serializers.ModelSerializer):
    type = TypeSerializer()  # Nested TypeSerializer
    categories = CategorySerializer(many=True)  # Nested CategorySerializer

    class Meta:
        model = BaseProduct
        fields = ['id', 'name', 'slug', 'description', 'price', 'quantity', 'status', 'type',
                  'image', 'gallery', 'product_type', 'translated_languages', 'discount', 'categories']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        return data


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProduct
        fields = ['id', 'name', 'slug', 'description', 'type', 'product_type', 'language',
                  'translated_languages', 'created_by']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        # data['max_price'] = Decimal(data['max_price'])
        # data['min_price'] = Decimal(data['min_price'])
        return data


# class ProductPagedDataSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Product
#         fields = ['id', 'price', 'sale_price', 'min_price', 'name']
#
#     def get_name(self, product):
#         base_product_data = product.get('base_product')
#
#         if base_product_data:
#             return base_product_data.get('name')
#         return None

class ProductPagedDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    sale_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    status = serializers.CharField()
    quantity = serializers.IntegerField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['price'] = Decimal(data['price'])
        return data

    def create(self, validated_data):
        # This method is not needed for serialization
        pass

    def update(self, instance, validated_data):
        # This method is not needed for serialization
        pass


class ProductionCombinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product', 'combination_string', 'price', 'sale_price', 'min_price', 'max_price', 'status',
                  'popular_product', 'discount', 'in_stock', 'unique_string_id', 'available_stock', 'created_by']

        # read_only_fields = ['id', 'created_by', 'updated_at']

        @staticmethod
        def create(validated_data):
            # Perform custom creation logic here if needed
            return Product.objects.create(**validated_data)

        @staticmethod
        def update(instance, validated_data):
            # Perform custom update logic here if needed
            instance.combination_string = validated_data.get('combination_string', instance.combination_string)
            instance.price = validated_data.get('price', instance.price)
            instance.sale_price = validated_data.get('sale_price', instance.sale_price)
            instance.min_price = validated_data.get('min_price', instance.min_price)
            instance.max_price = validated_data.get('max_price', instance.max_price)
            instance.status = validated_data.get('status', instance.status)
            instance.popular_product = validated_data.get('popular_product', instance.popular_product)
            instance.discount = validated_data.get('discount', instance.discount)
            instance.in_stock = validated_data.get('in_stock', instance.in_stock)
            instance.unique_string_id = validated_data.get('unique_string_id', instance.unique_string_id)
            instance.available_stock = validated_data.get('available_stock', instance.available_stock)
            instance.save()
            return instance


class CreateProductSerializer(serializers.ModelSerializer):
    product_combination = ProductionCombinationSerializer(required=False, allow_null=True)

    class Meta:
        model = BaseProduct
        fields = ['id', 'name', 'slug', 'description', 'type', 'product_type', 'language',
                  'translated_languages', 'created_by', 'product_combination']


class ProductVariantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProductVariant
        fields = '__all__'


class ProductVariantOptionValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseProductVariantOption
        fields = '__all__'
