from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

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
