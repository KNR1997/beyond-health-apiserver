from django.db import transaction
from rest_framework import status
from rest_framework.response import Response

from accounts.models import UserAccount
from products.models import (VariantOption,
                             BaseProductVariant,
                             Variant,
                             BaseProductVariantOption,
                             Product,
                             BaseProduct, Type)
from products.serializers import (ProductSerializer,
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


def create_simple_product_v2(request):
    try:
        user = UserAccount.objects.get(pk=request.data.get('created_by'))
        type_instance = Type.objects.get(pk=request.data.get('type'))

        with transaction.atomic():
            category_ids = request.data.get('categories', [])  # Get the list of category IDs from request data
            base_product = BaseProduct.objects.create(name=request.data.get('name'),
                                                      slug=request.data.get('slug'),
                                                      description=request.data.get('description'),
                                                      type=type_instance,
                                                      product_type=request.data.get('product_type'),
                                                      language=request.data.get('language'),
                                                      unit=request.data.get('unit'),
                                                      # translated_languages=request.data.get('translated_languages'),
                                                      # categories=request.data.get('categories'),
                                                      price=request.data.get('price'),
                                                      # sale_price=request.data.get('sale_price'),
                                                      created_by=user)
            base_product.categories.add(*category_ids)

            product = Product.objects.create(base_product=base_product,
                                             price=request.data.get('price'),
                                             sale_price=request.data.get('sale_price'),
                                             sku=request.data.get('sku'),
                                             quantity=request.data.get('quantity'),
                                             created_by=user)

            # Serialize the base_product instance
            base_product_serializer = BaseProductSerializer(base_product)

            # Return serialized base_product data in the response
            return Response(base_product_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Handle any exception that occurred during the transaction
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_variant_product_v2(request):
    try:
        user = UserAccount.objects.get(pk=request.data.get('created_by'))
        type_instance = Type.objects.get(pk=request.data.get('type'))
        variant_products = request.data.get('variation_options')
        upserts = variant_products.get('upsert')

        with transaction.atomic():
            category_ids = request.data.get('categories', [])  # Get the list of category IDs from request data
            base_product = BaseProduct.objects.create(name=request.data.get('name'),
                                                      slug=request.data.get('slug'),
                                                      description=request.data.get('description'),
                                                      type=type_instance,
                                                      unit=request.data.get('unit'),
                                                      product_type=request.data.get('product_type'),
                                                      language=request.data.get('language'),
                                                      min_price=request.data.get('min_price'),
                                                      max_price=request.data.get('max_price'),
                                                      quantity=request.data.get('quantity'),
                                                      price=request.data.get('price'),
                                                      created_by=user)
            base_product.categories.add(*category_ids)
            for upsert in upserts:
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
                        base_product_variant_option = BaseProductVariantOption.objects.create(base_product=base_product,
                                                                                              base_product_variant=base_product_variant,
                                                                                              variant_option=variant_option,
                                                                                              base_product_name=base_product.name,
                                                                                              variant_name=variant.name,
                                                                                              variant_option_name=variant_option.value)
                product = Product.objects.create(base_product=base_product,
                                                 price=upsert.get('price'),
                                                 sale_price=upsert.get('sale_price'),
                                                 sku=upsert.get('sku'),
                                                 title=upsert.get('title'),
                                                 quantity=upsert.get('quantity'),
                                                 created_by=user)
                product.base_product_variant_options.add(base_product_variant_option)
        # Serialize the base_product instance
        base_product_serializer = BaseProductSerializer(base_product)

        # Return serialized base_product data in the response
        return Response(base_product_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # Handle any exception that occurred during the transaction
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    base_product_variant_option = BaseProductVariantOption.objects.create(base_product=base_product,
                                                                                          base_product_variant=base_product_variant,
                                                                                          variant_option=variant_option,
                                                                                          base_product_name=base_product.name,
                                                                                          variant_name=variant.name,
                                                                                          variant_option_name=variant_option.value)

                product = Product.objects.create(base_product=base_product,
                                                 price=upsert.get('price'),
                                                 sale_price=upsert.get('sale_price'),
                                                 sku=upsert.get('sku'),
                                                 title=upsert.get('title'),
                                                 quantity=upsert.get('quantity'),
                                                 created_by=user)
                product.base_product_variant_options.add(base_product_variant_option)

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
    variations = request.data.get('variations')
    variant_products = request.data.get('variation_options')
    upserts = variant_products.get('upsert')
    deletes = variant_products.get('delete')
    user = UserAccount.objects.get(pk=request.data.get('created_by'))

    # List to hold response data for each product (updated or created)
    response_data = []
    try:
        with transaction.atomic():
            for delete in deletes:
                Product.objects.get(pk=delete).delete()
                # BaseProductVariant.objects.filter(base_product=base_product.id).delete()
                BaseProductVariantOption.objects.filter(base_product=base_product.id).delete()

            for upsert in upserts:
                if not upsert:
                    continue

                upsert_id = upsert.get('id')

                if upsert_id:
                    # Update existing product
                    try:
                        product = Product.objects.get(pk=upsert.get('id'))
                        product_serializer = ProductSerializer(instance=product, data=upsert, partial=True)

                        if product_serializer.is_valid():
                            # Save the updated or newly created product
                            updated_product = product_serializer.save()

                            # Append serialized product data to response list
                            response_data.append(ProductSerializer(updated_product).data)
                        else:
                            # If serializer is invalid, collect errors
                            return Response({'error': product_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

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
                                base_product_variant_option = BaseProductVariantOption.objects.create(
                                    base_product=base_product,
                                    base_product_variant=base_product_variant,
                                    variant_option=variant_option,
                                    base_product_name=base_product.name,
                                    variant_name=variant.name,
                                    variant_option_name=variant_option.value)
                                product.base_product_variant_options.add(base_product_variant_option)

                    except Product.DoesNotExist:
                        return Response(
                            {'error': f'Product with id {upsert.get('id')} does not exist for this base product.'},
                            status=status.HTTP_404_NOT_FOUND)
                else:
                    product = Product.objects.create(base_product=base_product,
                                                     price=upsert.get('price'),
                                                     sale_price=upsert.get('sale_price'),
                                                     sku=upsert.get('sku'),
                                                     title=upsert.get('title'),
                                                     quantity=upsert.get('quantity'),
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
                            base_product_variant_option = BaseProductVariantOption.objects.get(
                                base_product=base_product,
                                variant_name=option_name,
                                variant_option_name=option_value)
                        except BaseProductVariantOption.DoesNotExist:
                            # Create a new BaseProductVariantOption if it doesn't exist
                            base_product_variant_option = BaseProductVariantOption.objects.create(
                                base_product=base_product,
                                base_product_variant=base_product_variant,
                                variant_option=variant_option,
                                base_product_name=base_product.name,
                                variant_name=variant.name,
                                variant_option_name=variant_option.value)
                        product.base_product_variant_options.add(base_product_variant_option)

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
