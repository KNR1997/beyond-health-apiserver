from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product, VariantOption, BaseProductVariant, BaseProduct, Variant, BaseProductVariantOption, \
    Type
from products.serializers import BaseProductSerializer, CreateProductSerializer, ProductVariantSerializer, \
    ProductsPagedDataSerializer, ProductVariantOptionSerializer, ProductSerializer, \
    CustomVariantOptionSerializer, TypeSerializer, \
    CategorySerializer
from products.services.product_services import create_product_variant


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
        serializer = ProductsPagedDataSerializer(serialized_data, many=True)

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

        # Todo -> Save only if all requirements succeed
        base_product_instance = base_product_serializer.save()

        if product_type == 'variable':
            variant_options = request.data.get('variation_options')
            upserts = variant_options.get('upsert')

            for upsert in upserts:
                # get variant id using variant_option_data(integer)
                options = upsert.get('options')

                variant_option_keys = []

                # Get variant_options keys for product
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

                        # Create ProductVariant
                        variant_option_serializer = ProductVariantSerializer(data=base_product_variant_data)
                        if variant_option_serializer.is_valid():
                            base_product_variant_instance = variant_option_serializer.save()
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
                        variant_option_serializer = ProductVariantOptionSerializer(
                            data=base_product_variant_option_data)
                        if variant_option_serializer.is_valid():
                            variant_option_serializer.save()
                        else:
                            base_product_variant_instance.delete()
                            return Response(variant_option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Generate combination string based on variant option keys
                combination_string = generate_combination_string(variant_option_keys)

                product_data = {
                    'product': base_product_instance.id,
                    'combination_string': combination_string,
                    'product_type': base_product_instance.product_type,
                    **upsert,
                    'created_by': request.user.id,
                    # **request.data,  # Include all keys from request.data
                    # Add other fields as needed
                }

                product_serializer = ProductSerializer(data=product_data)
                if not product_serializer.is_valid():
                    base_product_instance.delete()  # Rollback product creation if combination fails
                    return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                product_serializer.save()

        if product_type == 'simple':
            # Create ProductionCombination for simple product
            product_data = {
                'product': base_product_instance.id,
                'combination_string': base_product_instance.name,
                **request.data,  # Include all keys from request.data
                # Add other fields as needed
            }

            # combination_serializer = ProductionCombinationSerializer(data=product_data)
            product_serializer = ProductSerializer(data=product_data)
            if not product_serializer.is_valid():
                base_product_instance.delete()  # Rollback product creation if combination fails
                return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            combination_instance = product_serializer.save()

            # Return response with combination data
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle other product types (e.g., variable product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_product(request, pk):
    try:
        # Retrieve the base_product instance from the database
        base_product = BaseProduct.objects.get(pk=pk)

        # Extract the existing product_type from the BaseProduct instance
        existing_product_type = base_product.product_type

        # Extract the product_type from the incoming request data
        requested_product_type = request.data.get('product_type')

        # Is update_product going to change its product_type (ex: simple to variable)
        if existing_product_type != requested_product_type:
            # Product type has changed, handle the change logic here
            # Example: If product_type is changing, you might need to update related data

            # You can implement specific logic based on the change in product_type
            # For example:
            # if existing_product_type == 'simple' and requested_product_type == 'variable':
            #     # Handle change from simple to variable product type
            #     pass
            # elif existing_product_type == 'variable' and requested_product_type == 'simple':
            #     # Handle change from variable to simple product type
            #     pass

            # Update the BaseProduct instance with the new data
            base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
            if base_product_serializer.is_valid():
                base_product_serializer.save()  # Save the updated BaseProduct instance
                return Response(base_product_serializer.data)
            else:
                return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # update_product not going to change its product_type
        else:
            # If product is a simple
            if existing_product_type == 'simple':
                # Product type has not changed, proceed with updating the existing BaseProduct
                base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
                if base_product_serializer.is_valid():
                    base_product_serializer.save()  # Save the updated BaseProduct instance
                    return Response(base_product_serializer.data)
                else:
                    return Response(base_product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # if product is variable
            else:
                base_product_serializer = BaseProductSerializer(instance=base_product, data=request.data, partial=True)
                if base_product_serializer.is_valid():
                    # Save the updated BaseProduct instance
                    base_product_instance = base_product_serializer.save()

                    # Get variant products from request data
                    variant_products = request.data.get('variation_options')
                    upserts = variant_products.get('upsert')

                    for upsert in upserts:
                        upsert_id = upsert.get('id')
                        # create new product
                        if upsert_id is None:
                            # create new Product
                            created_product = create_product_variant(base_product_instance, upsert, request)
                            if isinstance(created_product, Response):  # Check if creation failed
                                return created_product  # Return the error response

                        # update existing product
                        else:
                            product = Product.objects.get(pk=upsert.get('id'))
                            product_serializer = ProductSerializer(instance=product, data=upsert, partial=True)
                            if product_serializer.is_valid():
                                product_serializer.save()
                            else:
                                # Rollback the base product update if any variant product fails to save
                                # base_product_instance.delete()
                                return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

        # Todo -> get related_products
        # related_products = BaseProduct.objects.filter(type__slug=base_product.type.slug)[:20]

        # Serialize the product and related products
        base_product_serializer = BaseProductSerializer(base_product)
        product_type = Type.objects.get(pk=base_product.type_id)
        type_serializer = TypeSerializer(product_type)

        # Get all categories associated with the base_product
        categories = base_product.categories.all()

        # Serialize the categories
        category_serializer = CategorySerializer(categories, many=True)

        # if base_product is a variant product get the products
        if base_product.product_type == 'variable':
            # If the base product is a variant product, retrieve associated variants and options
            products = Product.objects.filter(product=base_product.id)
            product_variants = ProductSerializer(products, many=True)
            base_product_variation_options = BaseProductVariantOption.objects.filter(product_name=base_product.name)

            # get variant_options for the product
            variant_options_set = []
            for base_product_variation_option in base_product_variation_options:
                variant_option = VariantOption.objects.get(value=base_product_variation_option.variant_option_name)
                variant_options = VariantOption.objects.filter(variant_name=base_product_variation_option.variant_name)
                variant = Variant.objects.get(pk=variant_option.variant_id)

                custom_variant_data = {
                    'name': variant.name,
                    'shop_id': variant.shop_id,
                    'language': variant.language,
                    'translated_languages': variant.translated_languages,
                    'slug': variant.slug,
                    'values': variant_options,
                }

                combined_data = {
                    'id': variant_option.id,
                    'attribute': custom_variant_data,
                    'attribute_id': variant.id,
                    'name': variant_option.variant_name,
                    'language': variant_option.language,
                    'meta': variant_option.meta,
                    'slug': variant_option.slug,
                    'translated_languages': variant_option.translated_languages,
                    'value': variant_option.value,
                }
                variant_options_set.append(combined_data)

            variant_options_serializers = CustomVariantOptionSerializer(variant_options_set, many=True)

            # Add variations and variant options to the response data
            response_data = {
                **base_product_serializer.data,
                'type': type_serializer.data,
                'categories': category_serializer.data,
                'variations': variant_options_serializers.data,
                'variation_options': product_variants.data,
            }
        # if product is simple
        else:
            product = Product.objects.get(product=base_product.id)
            product_serializer = ProductSerializer(product)

            response_data = {
                **base_product_serializer.data,
                'sale_price': product_serializer.data['sale_price'],
                'sku': product_serializer.data['sku'],
                'categories': category_serializer.data,
                'type': type_serializer.data,
            }
        return Response(response_data)

    except BaseProduct.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['DELETE'])
def delete_product(request, pk):
    try:
        # Retrieve the product instance from the database
        base_product = get_object_or_404(BaseProduct, pk=pk)

        # Delete the product
        base_product.delete()

        return Response({'message': 'Product deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
