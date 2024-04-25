from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from products.models import Type
from products.serializers import TypeSerializer


@api_view(['GET'])
def get_types(request):
    try:
        # Get query parameters
        query_params = request.query_params
        limit = int(query_params.get('limit', 20))
        language = query_params.get('language')

        # Get all types
        types = Type.objects.all()

        # Apply language filter if provided
        if language:
            types = types.filter(language=language)

        # Paginate results
        paginator = Paginator(types, limit)
        paginated_types = paginator.get_page(paginator)

        # Serialize the paginated types
        serializer = TypeSerializer(paginated_types, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_type(request):
    return 0


@api_view(['PUT'])
def update_type(request, pk):
    return 0


@api_view(['DELETE'])
def delete_type(request, pk):
    return 0
