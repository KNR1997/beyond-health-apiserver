from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, VariantOption, BaseProductVariant, BaseProduct, Variant, BaseProductVariantOption
from products.serializers import BaseProductSerializer, CreateProductSerializer, ProductionCombinationSerializer, \
    ProductVariantOptionSerializer, ProductPagedDataSerializer, ProductVariantOptionValueSerializer, VariantSerializer, \
    VariantOptionSerializer


# Create your views here.


@api_view(['GET'])
def get_products(request):
    try:
        # Get query parameters
        query_params = request.query_params
        limit = int(query_params.get('limit', 20))
        page = int(query_params.get('page', 1))
        search = query_params.get('search')
        search_join = query_params.get('searchJoin', 'and')  # Default to 'and' if not provided
        with_fields = query_params.get('with', '').split(';')
        language = query_params.get('language')
        # order_by = query_params.get('orderBy', 'created_at')
        order_by = query_params.get('orderBy')
        sorted_by = query_params.get('sortedBy', 'desc')

        # Get all the products
        # products = Product.objects.all()
        base_products = BaseProduct.objects.all()

        # Apply search filter
        # if search:
        #     search_filters = {}
        #     for param in search.split(';'):
        #         key, value = param.split(':')
        #         search_filters[key] = value
        #
        #     # Then apply the filters to the queryset based on search join condition
        #     if search_join == 'and':
        #         products = products.filter(**search_filters)
        #     elif search_join == 'or':
        #         # Construct a Q object for 'or' conditions
        #         from django.db.models import Q
        #         or_query = Q()
        #         for key, value in search_filters.items():
        #             or_query |= Q(**{key: value})
        #         products = products.filter(or_query)

        # Apply 'with' fields
        # if with_fields:
        #     products = products.select_related(*with_fields)

        # Apply language filter if provided
        # if language:
        #     products = products.filter(language=language)

        # Apply sorting
        if sorted_by == 'asc':
            order_by = f"{order_by}"
        else:
            order_by = f"-{order_by}"

        # products = products.order_by(order_by)
        base_products = base_products.order_by(order_by)

        # Paginate results
        paginator = Paginator(base_products, limit)
        paginated_products = paginator.get_page(page)

        # Prepare data to serialize
        serialized_data = []
        for base_product in paginated_products:
            # Retrieve Base_product details for each product
            # product = Product.objects.get(pk=base_product.id)  # Adjust based on your model relationships

            # Construct combined data object
            combined_data = {
                # **base_product,
                # **product
                'id': base_product.id,
                'name': base_product.name,
                'description': base_product.description,
                'product_type': base_product.product_type,
                'slug': base_product.slug,
                'price': base_product.price,
                'max_price': base_product.max_price,
                'min_price': base_product.min_price,
                'quantity': base_product.quantity,
                'status': base_product.status,
            }
            serialized_data.append(combined_data)

        # Serialize the paginated products
        serializer = ProductPagedDataSerializer(serialized_data, many=True)

        # Construct next page URL
        next_page_url = None
        if paginated_products.has_next():
            next_page_url = f"{request.path}?{query_params.urlencode()}&page={page + 1}"

        # Construct previous page URL
        previous_page_url = None
        if paginated_products.has_previous():
            previous_page_url = f"{request.path}?{query_params.urlencode()}&page={page - 1}"

        return Response({
            'data': serializer.data,
            'next': next_page_url,
            'previous': previous_page_url
        })

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def generate_combination_string(variant_option_keys):
    # Sort the variant_option_keys alphabetically
    sorted_keys = sorted(variant_option_keys)
    # Join the sorted keys to form the combination string
    return ''.join(sorted_keys)


@api_view(['POST'])
def create_product(request):
    serializer = CreateProductSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        data = serializer.validated_data
        product_type = data.get('product_type', 'simple')

        # Create the base product
        base_product_serializer = BaseProductSerializer(data=request.data)
        if not base_product_serializer.is_valid():
            return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        base_product_instance = base_product_serializer.save()

        if product_type == 'variable':
            variant_options = request.data.get('variation_options')
            upserts = variant_options.get('upsert')

            for upsert in upserts:
                # get variant id using variant_option_data(integer)
                options = upsert.get('options')
                price = upsert.get('price')
                quantity = upsert.get('quantity')

                variant_option_keys = []

                for option in options:
                    variant = Variant.objects.get(name=option.get('name'))
                    variant_option = VariantOption.objects.get(value=option.get('value'))

                    # variant_option = VariantOption.objects.get(id=upsert)
                    option_id = variant_option.id
                    variant_option_first_letters = variant_option.first_letters
                    variant_option_keys.append(variant_option_first_letters)

                    # check if already Base_product has relation with variant
                    existing_relation = BaseProductVariant.objects.filter(
                        product=base_product_instance,
                        variant=variant
                    )

                    if not existing_relation:
                        base_product_variant_data = {
                            'product': base_product_instance.id,
                            'product_name': base_product_instance.name,
                            'variant': variant_option.variant.id,
                            'variant_name': variant_option.variant.name,
                        }

                        # Create ProductVariantOption
                        variant_option_serializer = ProductVariantOptionSerializer(data=base_product_variant_data)
                        if variant_option_serializer.is_valid():
                            base_product_variant_instance = variant_option_serializer.save(
                                product=base_product_instance)
                        else:
                            return Response(variant_option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    else:
                        base_product_variant_instance = BaseProductVariant.objects.get(
                            product=base_product_instance,
                            variant=variant_option.variant
                        )

                    # check if already Base_product has relation with variant_option
                    existing_product_variant_option = BaseProductVariantOption.objects.filter(
                        productVariationOption=base_product_variant_instance,
                        variant_option=variant_option
                    )

                    if not existing_product_variant_option:
                        base_product_variant_option_data = {
                            'productVariationOption': base_product_variant_instance.id,
                            'product_name': base_product_instance.name,
                            'variant_option': option_id,
                            'variant_name': variant_option.variant.name,
                            'variant_option_name': variant_option.value,
                        }

                        # Create ProductVariantOption
                        variant_option_serializer = ProductVariantOptionValueSerializer(
                            data=base_product_variant_option_data)
                        if variant_option_serializer.is_valid():
                            variant_option_serializer.save()
                        else:
                            base_product_variant_instance.delete()
                            return Response(variant_option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                    # base_product_variant_option_value = {
                    #     'productVariationOption': base_product_variant_instance.id,
                    #     'product_name': base_product_instance.name,
                    #     'variant_option': option_id,
                    #     'variant_name': variant_option.variant.name,
                    #     'variant_option_name': variant_option.value,
                    # }
                    #
                    # variant_option_value_serializer = ProductVariantOptionValueSerializer(
                    #     data=base_product_variant_option_value)
                    #
                    # if variant_option_value_serializer.is_valid():
                    #     variant_option_value_serializer.save()
                    # else:
                    #     base_product_variant_instance.delete()
                    #     return Response(variant_option_value_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Generate combination string based on variant option keys
                combination_string = generate_combination_string(variant_option_keys)

                combination_data = {
                    'product': base_product_instance.id,
                    'combination_string': combination_string,
                    **upsert,
                    'created_by': request.user.id,
                    # **request.data,  # Include all keys from request.data
                    # Add other fields as needed
                }

                combination_serializer = ProductionCombinationSerializer(data=combination_data)
                if not combination_serializer.is_valid():
                    base_product_instance.delete()  # Rollback product creation if combination fails
                    return Response(combination_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                combination_instance = combination_serializer.save()

        if product_type == 'simple':
            # Create ProductionCombination for simple product
            combination_data = {
                'product': base_product_instance.id,
                'combination_string': base_product_instance.name,
                **request.data,  # Include all keys from request.data
                # Add other fields as needed
            }

            combination_serializer = ProductionCombinationSerializer(data=combination_data)
            if not combination_serializer.is_valid():
                base_product_instance.delete()  # Rollback product creation if combination fails
                return Response(combination_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            combination_instance = combination_serializer.save()

            # Return response with combination data
            return Response(combination_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle other product types (e.g., variable product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_product(request, pk):
    try:
        # Retrieve the product instance from the database
        # product = Product.objects.get(pk=pk)
        base_product = BaseProduct.objects.get(pk=pk)

        # Deserialize the request data to update the product instance
        base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
        if base_product_serializer.is_valid():
            base_product_serializer.save()  # Save the updated product instance
            return Response(base_product_serializer.data)
        else:
            return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_product_by_slug(request, slug):
    try:
        # Retrieve the product based on the provided slug
        base_product = get_object_or_404(BaseProduct, slug=slug)

        # Retrieve related products
        related_products = BaseProduct.objects.filter(type__slug=base_product.type.slug)[:20]

        # Serialize the product and related products
        product_serializer = BaseProductSerializer(base_product)

        # if base_product is a variant product get the products
        if base_product.product_type == 'variable':
            # If the base product is a variant product, retrieve associated variants and options
            variants = BaseProductVariant.objects.filter(product=base_product.id)
            # variant_options = BaseProductVariantOption.objects.filter(variant__in=variants)

            # Serialize variants and variant options
            # variant_serializer = VariantSerializer(variants, many=True)
            # variant_option_serializer = VariantOptionSerializer(variant_options, many=True)

            variant_options = {

            }

            # Add variations and variant options to the response data
            response_data = {
                **product_serializer.data,
                # 'variations': variant_serializer.data,
                # 'variant_options': variant_option_serializer.data,
            }
        else:
            # If the base product is not a variant product, return the product data without variations
            response_data = product_serializer.data
        return Response(response_data)
        # related_products_serializer = BaseProductSerializer(related_products, many=True)

        # Construct the response data using dictionary unpacking
        # response_data = {
        #     **product_serializer.data,
        #     'variations': ,
        #     'variant_options': ,
        #     # 'related_products': related_products_serializer.data
        # }
        #
        # return Response(response_data)

    except BaseProduct.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        # Retrieve the product instance from the database
        product = get_object_or_404(Product, pk=pk)

        # Delete the product
        product.delete()

        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
