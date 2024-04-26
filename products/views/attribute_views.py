from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from products.models import Variant
from products.serializers import VariantSerializer
from django.db.models import Q

from rest_framework.decorators import api_view


@api_view(['GET'])
def get_variants(request):
    try:
        # Get query parameters
        query_params = request.query_params
        limit = int(query_params.get('limit', 30))
        page = int(query_params.get('page', 1))
        search = query_params.get('search')
        search_join = query_params.get('searchJoin', 'and')
        language = query_params.get('language')
        # order_by = query_params.get('orderBy')
        sorted_by = query_params.get('sortedBy', 'desc')

        # Get all attributes
        variants = Variant.objects.all()

        # Apply search filter
        if search:
            search_filters = {}
            for param in search.split(';'):
                key, value = param.split(':')
                search_filters[key] = value

            # Then apply the filters to the queryset based on search join condition
            if search_join == 'and':
                attributes = variants.filter(**search_filters)
            elif search_join == 'or':
                # Construct a Q object for 'or' conditions
                or_query = Q()
                for key, value in search_filters.items():
                    or_query |= Q(**{key: value})
                attributes = variants.filter(or_query)

        # Apply language filter if provided
        if language:
            attributes = attributes.filter(language=language)

        # Apply sorting
        # if sorted_by == 'asc':
        #     order_by = f"{order_by}"
        # else:
        #     order_by = f"-{order_by}"
        #
        # attributes = attributes.order_by(order_by)

        # Paginate results
        paginator = Paginator(attributes, limit)
        paginated_attributes = paginator.get_page(page)

        # Serialize the paginated attributes
        serializer = VariantSerializer(paginated_attributes, many=True)

        # Construct next page URL
        next_page_url = None
        if paginated_attributes.has_next():
            next_page_url = f"{request.path}?{request.query_params.urlencode()}&page={page + 1}"

        # Construct previous page URL
        previous_page_url = None
        if paginated_attributes.has_previous():
            previous_page_url = f"{request.path}?{request.query_params.urlencode()}&page={page - 1}"

        # return Response({
        #     serializer.data
        #     # 'data': serializer.data,
        #     # 'next': next_page_url,
        #     # 'previous': previous_page_url
        # })

        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
