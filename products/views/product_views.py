from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, VariantOption, BaseProductVariant, BaseProduct
from products.serializers import BaseProductSerializer, CreateProductSerializer, ProductDetailSerializer, \
    ProductionCombinationSerializer, ProductVariantOptionSerializer, ProductVariantOptionValueSerializer, \
    ProductPagedDataSerializer


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
        products = Product.objects.all()

        # Apply search filter
        if search:
            search_filters = {}
            for param in search.split(';'):
                key, value = param.split(':')
                search_filters[key] = value

            # Then apply the filters to the queryset based on search join condition
            if search_join == 'and':
                products = products.filter(**search_filters)
            elif search_join == 'or':
                # Construct a Q object for 'or' conditions
                from django.db.models import Q
                or_query = Q()
                for key, value in search_filters.items():
                    or_query |= Q(**{key: value})
                products = products.filter(or_query)

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

        products = products.order_by(order_by)

        # Paginate results
        paginator = Paginator(products, limit)
        paginated_products = paginator.get_page(page)

        # Prepare data to serialize
        serialized_data = []
        for product in paginated_products:
            # Retrieve Base_product details for each product
            base_product = BaseProduct.objects.get(pk=product.product_id)  # Adjust based on your model relationships

            # Construct combined data object
            combined_data = {
                'id': product.id,
                'name': base_product.name,
                'description': base_product.description,
                'price': product.price,
                'sale_price': product.sale_price,
                'min_price': product.min_price,
                'quantity': product.quantity,
                'status': product.status,
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

        if product_type == 'variant':
            variant_options = request.data.get('variant_options')
            variant_option_keys = []

            for variant_option_data in variant_options:
                # get variant id using variant_option_data(integer)
                variant_option = VariantOption.objects.get(id=variant_option_data)
                option_id = variant_option.id
                variant_option_first_letters = variant_option.first_letters
                variant_option_keys.append(variant_option_first_letters)

                # check if already Base_product has relation with variant
                existing_relation = BaseProductVariant.objects.filter(
                    product=base_product_instance,
                    variant=variant_option.variant
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
                        base_product_variant_instance = variant_option_serializer.save(product=base_product_instance)
                    else:
                        return Response(variant_option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    base_product_variant_instance = BaseProductVariant.objects.get(
                        product=base_product_instance,
                        variant=variant_option.variant
                    )

                base_product_variant_option_value = {
                    'productVariationOption': base_product_variant_instance.id,
                    'product_name': base_product_instance.name,
                    'variant_option': option_id,
                    'variant_name': variant_option.variant.name,
                    'variant_option_name': variant_option.value,
                }

                variant_option_value_serializer = ProductVariantOptionValueSerializer(
                    data=base_product_variant_option_value)

                if variant_option_value_serializer.is_valid():
                    variant_option_value_serializer.save()
                else:
                    base_product_variant_instance.delete()
                    return Response(variant_option_value_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Generate combination string based on variant option keys
            combination_string = generate_combination_string(variant_option_keys)

            combination_data = {
                'product': base_product_instance.id,
                'combination_string': combination_string,
                **request.data,  # Include all keys from request.data
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
        product = Product.objects.get(pk=pk)

        # Deserialize the request data to update the product instance
        serializer = BaseProductSerializer(instance=product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save the updated product instance
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_product_by_slug(request, slug):
    try:
        # Retrieve the product based on the provided slug
        product = get_object_or_404(Product, slug=slug)

        # Retrieve related products
        related_products = Product.objects.filter(type__slug=product.type.slug)[:20]

        # Serialize the product and related products
        product_serializer = BaseProductSerializer(product)
        related_products_serializer = BaseProductSerializer(related_products, many=True)

        # Construct the response data using dictionary unpacking
        response_data = {
            **product_serializer.data,
            'related_products': related_products_serializer.data
        }

        return Response(response_data)

    except Product.DoesNotExist:
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
