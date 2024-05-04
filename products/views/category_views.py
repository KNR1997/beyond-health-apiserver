from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Category
from products.serializers import CategorySerializer


@api_view(['GET'])
def get_categories(request):
    try:
        # Get query parameters from the request
        query_params = request.query_params
        limit = int(query_params.get('limit', 20))
        page_number = int(query_params.get('page', 1))
        language = query_params.get('language')
        search_join = query_params.get('searchJoin', 'and')
        order_by = query_params.get('orderBy', 'created_at')
        sorted_by = query_params.get('sortedBy', 'desc')
        search = query_params.get('search')

        # Get all categories
        categories = Category.objects.all()

        # Apply language filter if provided
        if language:
            categories = categories.filter(language=language)

        # Apply search filter if provided
        # if search:
        #     # Split the search string into field and value
        #     field, value = search.split(':')
        #
        #     # Apply appropriate search join logic (default to 'and' if invalid)
        #     if search_join.lower() == 'and':
        #         search_filters = {f'{field}__icontains': value}
        #         categories = categories.filter(**search_filters)
        #     elif search_join.lower() == 'or':
        #         # Create a Q object for 'or' condition using |
        #         from django.db.models import Q
        #         search_filters = Q(**{f'{field}__icontains': value})
        #         categories = categories.filter(search_filters)

        # Apply sorting/ordering
        if sorted_by.lower() == 'asc':
            order_by = f"{order_by}"  # Ascending order
        else:
            order_by = f"-{order_by}"  # Descending order

        # Sort the queryset based on the order_by field
        categories = categories.order_by(order_by)

        # Paginate results
        paginator = Paginator(categories, limit)
        paginated_categories = paginator.get_page(page_number)

        # Serialize the paginated categories
        serializer = CategorySerializer(paginated_categories, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_category(request):
    try:
        # Deserialize request data into CategorySerializer
        serializer = CategorySerializer(data=request.data)

        # Validate the serializer data
        if serializer.is_valid():
            # Save the validated data to create a new Category instance
            serializer.save()

            # Return success response with serialized data of the created category
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Return error response with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Return error response if an exception occurs during creation process
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_category(request, pk):
    return 0


@api_view(['DELETE'])
def delete_category(request, pk):
    return 0
