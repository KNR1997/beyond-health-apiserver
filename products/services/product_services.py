from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from accounts.models import UserAccount
from products.models import (VariantOption,
                             BaseProductVariant,
                             Variant,
                             BaseProductVariantOption,
                             Product)
from products.serializers import (ProductSerializer,
                                  BaseProductVariantSerializer,
                                  BaseProductVariantOptionSerializer,
                                  BaseProductSerializer)


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


# todo -> rename to create_product_record_for_variable_product
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


def simple_product_to_variant_product_conversion(base_product, request):
    try:
        variation_options = request.data.get('variation_options')
        upserts = variation_options.get('upsert')
        user = UserAccount.objects.get(pk=request.data.get('created_by'))

        with transaction.atomic():
            # Delete the existing Product
            Product.objects.filter(base_product=base_product.id).delete()

            # Create BaseProductVariants, BaseProductVariantOptions and Product
            for upsert in upserts:
                product = Product(base_product=base_product,
                                  price=upsert.get('price'),
                                  sale_price=upsert.get('sale_price'),
                                  sku=upsert.get('sku'),
                                  title=upsert.get('title'),
                                  created_by=user)

                options = upsert.get('options', [])
                for option in options:
                    option_name = option.get('name')
                    option_value = option.get('value')

                    variant = Variant.objects.get(name=option_name)
                    variant_option = VariantOption.objects.get(value=option_value)

                    # create BaseProductVariants
                    base_product_variant = BaseProductVariant.objects.create(base_product=base_product,
                                                                             base_product_name=base_product.name,
                                                                             variant=variant,
                                                                             variant_name=option_name)
                    # create BaseProductVariantOptions
                    BaseProductVariantOption.objects.create(base_product=base_product,
                                                            base_product_variant=base_product_variant,
                                                            variant_option=variant_option,
                                                            base_product_name=base_product.name,
                                                            variant_name=variant.name,
                                                            variant_option_name=variant_option.value)

                product_serializer = ProductSerializer(instance=product, data=upsert, partial=True)

                if product_serializer.is_valid():
                    # Save the updated or newly created product
                    product_serializer.save()
                else:
                    # If serializer is invalid, collect errors
                    return Response({'error': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # If all products were updated or created successfully, save the base_product
            base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
            if base_product_serializer.is_valid():
                # Save the updated BaseProduct instance
                base_product_serializer.save()
            else:
                return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(base_product_serializer.data)

    except Exception as e:
        # Handle any exception that occurred during the transaction
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def variant_product_to_simple_product_conversion(base_product, request):
    try:
        variation_options = request.data.get('variation_options')
        user = UserAccount.objects.get(pk=request.data.get('created_by'))

        with transaction.atomic():
            # Delete the existing Products, BaseProductVariants, BaseProductVariantOptions
            Product.objects.filter(base_product=base_product.id).delete()
            BaseProductVariant.objects.filter(base_product=base_product.id).delete()
            BaseProductVariantOption.objects.filter(base_product=base_product.id).delete()

            # Create new Product
            Product.objects.create(base_product=base_product,
                                   combination_string=None,
                                   product_type=request.data.get('product_type'),
                                   sku=request.data.get('sku'),
                                   price=request.data.get('price'),
                                   sale_price=request.data.get('sale_price'),
                                   quantity=request.data.get('quantity'),
                                   status=request.data.get('status'),
                                   created_by=user)

            # Update BaseProduct
            base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
            if base_product_serializer.is_valid():
                # Save the updated BaseProduct instance
                base_product_serializer.save()
            else:
                return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(base_product_serializer.data)
    except Exception as e:
        # Handle any exception that occurred during the transaction
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_simple_product(base_product, request):
    product = Product.objects.get(base_product=base_product)

    # Serialize the base product with partial data
    base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
    product_serializer = ProductSerializer(instance=product, data=request.data, partial=True)

    # Check if both serializers are valid
    if base_product_serializer.is_valid() and product_serializer.is_valid():
        # Save the updated base product
        base_product_instance = base_product_serializer.save()

        # Save all related products
        product_instances = product_serializer.save()

        # Construct a response with updated data
        response_data = {
            'base_product': BaseProductSerializer(base_product_instance).data,
            'product': ProductSerializer(product_instances).data
        }
        return Response(base_product_serializer.data, status=status.HTTP_200_OK)

    # If any serializer is invalid, return the errors
    errors = {}
    if not base_product_serializer.is_valid():
        errors['base_product'] = base_product_serializer.errors
    if not product_serializer.is_valid():
        errors['product'] = product_serializer.errors

    return Response(errors, status=status.HTTP_400_BAD_REQUEST)


def update_variant_product(base_product, request):
    variant_products = request.data.get('variation_options')
    upserts = variant_products.get('upsert')
    user = UserAccount.objects.get(pk=request.data.get('created_by'))

    # List to hold response data for each product (updated or created)
    response_data = []

    try:
        with transaction.atomic():
            for upsert in upserts:
                upsert_id = upsert.get('id')

                if upsert_id:
                    # Update existing product
                    try:
                        product = Product.objects.get(pk=upsert.get('id'))
                    except Product.DoesNotExist:
                        return Response(
                            {'error': f'Product with id {upsert.get('id')} does not exist for this base product.'},
                            status=status.HTTP_404_NOT_FOUND)
                else:
                    product = Product(base_product=base_product,
                                      price=upsert.get('price'),
                                      sale_price=upsert.get('sale_price'),
                                      sku=upsert.get('sku'),
                                      title=upsert.get('title'),
                                      created_by=user)

                    # Process options to create or retrieve BaseProductVariant objects
                    options = upsert.get('options', [])
                    for option in options:
                        option_name = option.get('name')
                        option_value = option.get('value')

                        variant = Variant.objects.get(name=option_name)
                        variant_option = VariantOption.objects.get(value=option_value)

                        # Check if a BaseProductVariant already exists for the given name and value
                        try:
                            base_product_variant = BaseProductVariant.objects.get(base_product=base_product,
                                                                                  base_product_name=base_product.name,
                                                                                  variant=variant,
                                                                                  variant_name=option_name)

                        except BaseProductVariant.DoesNotExist:
                            # Create a new BaseProductVariant if it doesn't exist
                            base_product_variant = BaseProductVariant.objects.create(base_product=base_product,
                                                                                     base_product_name=base_product.name,
                                                                                     variant=variant,
                                                                                     variant_name=option_name)
                        try:
                            BaseProductVariantOption.objects.get(base_product=base_product,
                                                                 variant_name=option_name,
                                                                 variant_option_name=option_value)
                        except BaseProductVariantOption.DoesNotExist:
                            # Create a new BaseProductVariantOption if it doesn't exist
                            BaseProductVariantOption.objects.create(base_product=base_product,
                                                                    base_product_variant=base_product_variant,
                                                                    variant_option=variant_option,
                                                                    base_product_name=base_product.name,
                                                                    variant_name=variant.name,
                                                                    variant_option_name=variant_option.value)

                product_serializer = ProductSerializer(instance=product, data=upsert, partial=True)

                if product_serializer.is_valid():
                    # Save the updated or newly created product
                    updated_product = product_serializer.save()

                    # Append serialized product data to response list
                    response_data.append(ProductSerializer(updated_product).data)
                else:
                    # If serializer is invalid, collect errors
                    return Response({'error': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # If all products were updated or created successfully, save the base_product
            base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
            if base_product_serializer.is_valid():
                # Save the updated BaseProduct instance
                base_product_serializer.save()
            else:
                return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(base_product_serializer.data)

    except Exception as e:
        # Handle any exception that occurred during the transaction
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# def update_variant_product(base_product, request):
#     base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
#     if base_product_serializer.is_valid():
#         # Save the updated BaseProduct instance
#         base_product_instance = base_product_serializer.save()
#
#         # Get variant products from request data
#         variant_products = request.data.get('variation_options')
#         upserts = variant_products.get('upsert')
#
#         for upsert in upserts:
#             upsert_id = upsert.get('id')
#             # create new product
#             if upsert_id is None:
#                 # create new Product
#                 create_variable_products(base_product_instance, upsert, request.user.id)
#             # update existing product
#             else:
#                 product = Product.objects.get(pk=upsert.get('id'))
#                 product_serializer = ProductSerializer(instance=product, data=upsert, partial=True)
#                 if product_serializer.is_valid():
#                     product_serializer.save()
#                 else:
#                     # Rollback the base product update if any variant product fails to save
#                     # base_product_instance.delete()
#                     return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         return Response(base_product_serializer.data)
#     else:
#         return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     pass


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
