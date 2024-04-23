from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer


# Create your views here.


@api_view(['GET'])
def get_products(request):
    # try:
    #     # Get query parameters
    #     query_params = request.query_params
    #     limit = int(query_params.get('limit', 30))
    #     page = int(query_params.get('page', 1))
    #     search = query_params.get('searchJoin')
    #
    #     # Get all the products
    #     products = Product.objects.all()
    #
    #     # Apply search filter
    #     search_filters = {}
    #     for param in search.split(';'):
    #         key, value = param.split(':')
    #         if key == 'type.slug':  # Check if the key is 'type.slug'
    #             search_filters['type__slug'] = value  # Use '__' to traverse the relationship
    #         elif key != 'slug':
    #             search_filters[key] = value
    #
    #     # Then apply the filters to the queryset
    #     products = products.filter(**search_filters)
    #
    #     # Paginate results
    #     paginator = Paginator(products, limit)
    #     paginated_products = paginator.get_page(page)
    #
    #     # Serialize the paginated products
    #     serializer = ProductSerializer(paginated_products, many=True)
    #
    #     # Construct next page URL
    #     next_page_url = None
    #     if paginated_products.has_next():
    #         next_page_url = f"{request.path}?{query_params.urlencode()}&page={page + 1}"
    #
    #     # Construct previous page URL
    #     previous_page_url = None
    #     if paginated_products.has_previous():
    #         previous_page_url = f"{request.path}?{query_params.urlencode()}&page={page - 1}"
    #
    #     return Response({
    #         'data': serializer.data,
    #         'next': next_page_url,
    #         'previous': previous_page_url
    #     })
    #
    # except Exception as e:
    #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
        if language:
            products = products.filter(language=language)

        # Apply sorting
        if sorted_by == 'asc':
            order_by = f"{order_by}"
        else:
            order_by = f"-{order_by}"

        products = products.order_by(order_by)

        # Paginate results
        paginator = Paginator(products, limit)
        paginated_products = paginator.get_page(page)

        # Serialize the paginated products
        serializer = ProductSerializer(paginated_products, many=True)

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


@api_view(['PUT'])
def update_product(request, pk):
    try:
        # Retrieve the product instance from the database
        product = Product.objects.get(pk=pk)

        # Deserialize the request data to update the product instance
        serializer = ProductSerializer(instance=product, data=request.data, partial=True)
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
        product_serializer = ProductSerializer(product)
        related_products_serializer = ProductSerializer(related_products, many=True)

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
