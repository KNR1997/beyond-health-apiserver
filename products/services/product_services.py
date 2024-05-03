from rest_framework import status
from rest_framework.response import Response

from products.models import VariantOption, BaseProductVariant, Variant, BaseProductVariantOption
from products.serializers import ProductSerializer, BaseProductVariantSerializer, BaseProductVariantOptionSerializer, \
    BaseProductSerializer


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
            'base_product': base_product.id,
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
                base_product=base_product,
                variant=variant_instance,
            )

            if not existing_product_variant:
                base_product_variant_data = {
                    'base_product': base_product.id,
                    'base_product_name': base_product.name,
                    'variant': variant_instance.id,
                    'variant_name': variant_instance.name,
                }

                # Create ProductVariant
                variant_option_serializer = BaseProductVariantSerializer(data=base_product_variant_data)
                if variant_option_serializer.is_valid():
                    base_product_variant_instance = variant_option_serializer.save()
                else:
                    return Response(variant_option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                base_product_variant_instance = existing_product_variant.first()

            # check if already Base_product has relation with variant_option
            existing_product_variant_option = BaseProductVariantOption.objects.filter(
                base_product=base_product,
                variant_option_name=variant_option_instance.value
            )

            if not existing_product_variant_option:
                base_product_variant_option_data = {
                    'base_product': base_product.id,
                    'base_product_variant': base_product_variant_instance.id,
                    'variant_option': variant_option_instance.id,
                    'base_product_name': base_product.name,
                    'variant_name': variant_option_instance.variant_name,
                    'variant_option_name': variant_option_instance.value,
                }

                # Create ProductVariantOption
                base_product_variant_option = BaseProductVariantOptionSerializer(
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


def create_variable_products(base_product_instance, upserts, created_by):
    for upsert in upserts:
        variant_option_keys = []
        options = upsert.get('options')

        try:
            for option in options:
                variant_option = get_or_create_variant_option(option)
                variant_option_keys.append(variant_option.first_letters)

                # create product_variant
                base_product_variant_instance = create_base_product_variant(base_product_instance, variant_option)

                # create product_variant_option
                create_base_product_variant_option(
                    base_product_instance,
                    base_product_variant_instance,
                    variant_option,
                    base_product_instance.name,
                    variant_option.variant.name,
                    variant_option.value
                )

            combination_string = generate_combination_string(variant_option_keys)

            product_data = {
                'base_product': base_product_instance.id,
                'combination_string': combination_string,
                'product_type': base_product_instance.product_type,
                **upsert,
                'created_by': created_by,
            }
            save_product(product_data)

        except Exception as e:
            raise e
            # return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return a success response if all iterations complete without errors
    return Response({'message': 'Products created successfully'}, status=status.HTTP_201_CREATED)


def create_simple_product(base_product_instance, data):
    product_data = {
        'base_product': base_product_instance.id,
        'combination_string': None,
        **data,
    }
    save_product(product_data)


def update_simple_product(base_product, request):
    base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
    if base_product_serializer.is_valid():
        base_product_serializer.save()
        return Response(base_product_serializer.data)
    else:
        return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_or_create_variant_option(option_data):
    variant = Variant.objects.get(name=option_data.get('name'))
    variant_option, created = VariantOption.objects.get_or_create(value=option_data.get('value'))
    return variant_option


def create_base_product_variant(base_product_instance, variant_option):
    try:
        existing_relation = BaseProductVariant.objects.filter(
            base_product=base_product_instance,
            variant=variant_option.variant
        ).first()

        if existing_relation:
            return existing_relation

        # If no existing relation found, create a new BaseProductVariant instance
        base_product_variant_data = {
            'base_product': base_product_instance.id,
            'base_product_name': base_product_instance.name,
            'variant': variant_option.variant.id,
            'variant_name': variant_option.variant.name,
        }

        return save_base_product_variant(data=base_product_variant_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_base_product_variant_option(base_product_instance, base_product_variant_instance, variant_option,
                                       product_name, variant_name, variant_option_name):
    try:
        existing_product_variant_option = BaseProductVariantOption.objects.filter(
            base_product=base_product_instance,
            variant_option=variant_option
        ).exists()

        if not existing_product_variant_option:
            base_product_variant_option_data = {
                'base_product': base_product_instance.id,
                'base_product_variant': base_product_variant_instance.id,
                'variant_option': variant_option.id,
                'base_product_name': product_name,
                'variant_name': variant_name,
                'variant_option_name': variant_option_name,
            }

            save_base_product_variant_option(data=base_product_variant_option_data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def save_base_product(data):
    base_product_serializer = BaseProductSerializer(data=data)
    base_product_serializer.is_valid(raise_exception=True)
    return base_product_serializer.save()


def save_base_product_variant(data):
    base_product_variant_serializer = BaseProductVariantSerializer(data=data)
    base_product_variant_serializer.is_valid(raise_exception=True)
    return base_product_variant_serializer.save()


def save_base_product_variant_option(data):
    base_product_variant_option_serializer = BaseProductVariantOptionSerializer(data=data)
    base_product_variant_option_serializer.is_valid(raise_exception=True)
    return base_product_variant_option_serializer.save()


def save_product(product_data):
    product_serializer = ProductSerializer(data=product_data)
    product_serializer.is_valid(raise_exception=True)
    return product_serializer.save()
