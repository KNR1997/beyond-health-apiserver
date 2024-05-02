from rest_framework import status
from rest_framework.response import Response

from products.models import VariantOption, BaseProductVariant, Variant, BaseProductVariantOption
from products.serializers import ProductSerializer, ProductVariantSerializer, ProductVariantOptionSerializer


def generate_combination_string(variant_option_keys):
    # Sort the variant_option_keys alphabetically
    sorted_keys = sorted(variant_option_keys)
    # Join the sorted keys to form the combination string
    return ''.join(sorted_keys)


def get_combination_string(upsert_options):
    variant_option_keys = []
    for upsert_option in upsert_options:
        variant_option = VariantOption.objects.get(value=upsert_option.get('value'))
        variant_option_first_letters = variant_option.first_letters
        variant_option_keys.append(variant_option_first_letters)
    combination_string = generate_combination_string(variant_option_keys)

    return ''.join(combination_string)


def create_product_variant(base_product, upsert, request):
    # Retrieve or calculate the combination string based on variant options
    combination_string = get_combination_string(upsert.get('options', []))
    upsert_options = upsert.get('options', [])

    try:
        product_data = {
            'product': base_product.id,
            'combination_string': combination_string,
            'product_type': 'variable',
            'sku': upsert.get("sku"),
            'title': upsert.get("title"),
            'price': upsert.get("price"),
            'sale_price': upsert.get("sale_price"),
            'quantity': upsert.get("quantity"),
            'created_by': request.data.get("created_by"),
        }

        product_serializer = ProductSerializer(data=product_data)
        if not product_serializer.is_valid():
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Save the serializer to persist the product data
        product_serializer.save()

        # Todo -> create base_product_variant table record
        # Todo -> create base_product_variant_option record
        for option in upsert_options:
            # check if already Base_product has relation with variant
            variant_instance = Variant.objects.get(name=option.get('name'))
            variant_option_instance = VariantOption.objects.get(value=option.get('value'))
            base_product_variant_instance = None

            existing_product_variant = BaseProductVariant.objects.filter(
                product=base_product,
                variant=variant_instance,
            )

            if not existing_product_variant:
                base_product_variant_data = {
                    'product': base_product.id,
                    'product_name': base_product.name,
                    'variant': variant_instance.id,
                    'variant_name': variant_instance.name,
                }

                # Create ProductVariant
                variant_option_serializer = ProductVariantSerializer(data=base_product_variant_data)
                if variant_option_serializer.is_valid():
                    base_product_variant_instance = variant_option_serializer.save()
                else:
                    return Response(variant_option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                base_product_variant_instance = existing_product_variant.first()

            # check if already Base_product has relation with variant_option
            existing_product_variant_option = BaseProductVariantOption.objects.filter(
                productVariationOption=base_product_variant_instance,
                variant_option=variant_option_instance
            )

            if not existing_product_variant_option:
                base_product_variant_option_data = {
                    'productVariationOption': base_product_variant_instance.id,
                    'product_name': base_product.name,
                    'variant_option': variant_option_instance.id,
                    'variant_name': variant_option_instance.variant_name,
                    'variant_option_name': variant_option_instance.value,
                }

                # Create ProductVariantOption
                base_product_variant_option = ProductVariantOptionSerializer(
                    data=base_product_variant_option_data)
                if base_product_variant_option.is_valid():
                    base_product_variant_option.save()
                else:
                    base_product_variant_instance.delete()
                    return Response(base_product_variant_option.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                pass
        # Return a successful response with serialized product data
        # return Response(product_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Handle any exceptions and return a server error response
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
