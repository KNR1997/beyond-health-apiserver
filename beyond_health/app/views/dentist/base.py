# Third party imports
from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.app.permissions.base import allow_permission, ROLE
from beyond_health.app.serializers.dentist import DentistListSerializer, DentistSerializer
from beyond_health.db.models import Dentist


# Create your views here.
class DentistViewSet(BaseViewSet):
    model = Dentist
    serializer_class = DentistListSerializer

    search_fields = []
    filterset_fields = []

    lookup_field = "slug"

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        slug = kwargs.get("slug")
        course = self.get_queryset().filter(slug=slug).first()

        if not course:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = DentistSerializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
