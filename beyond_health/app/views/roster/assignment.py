from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.serializers.roster import RosterAssignmentListSerializer, RosterAssignmentCreateSerializer
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
            self.filter_queryset(super().get_queryset()).filter(roster_week_id=self.kwargs['pk'])
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = RosterAssignmentCreateSerializer(
            data={**request.data}
        )
        if serializer.is_valid():
            serializer = serializer.save()

            return Response(RosterAssignmentListSerializer(serializer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a roster assignment by ID"""
        try:
            assignment = RosterAssignment.objects.get(pk=pk)
            assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RosterAssignment.DoesNotExist:
            return Response(
                {"detail": "Roster assignment not found."},
                status=status.HTTP_404_NOT_FOUND
            )
