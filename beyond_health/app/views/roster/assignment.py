from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.serializers.roster import RosterAssignmentListSerializer, RosterAssignmentSerializer
from beyond_health.app.views.base import BaseViewSet
from beyond_health.db.models.roster import RosterAssignment


# Create your views here.
class RosterAssignmentViewSet(BaseViewSet):
    model = RosterAssignment
    serializer_class = RosterAssignmentListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = RosterAssignmentSerializer(
            data={**request.data}
        )
        if serializer.is_valid():
            serializer = serializer.save()

            return Response(RosterAssignmentListSerializer(serializer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
