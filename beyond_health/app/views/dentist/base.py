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

    search_fields = ['user__first_name','user__last_name']
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def create(self, request, *args, **kwargs):
        serializer = DentistSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dentist = serializer.save()

        output = DentistListSerializer(dentist, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    @allow_permission([ROLE.ADMIN])
    def update(self, request, *args, **kwargs):
        dentist = Dentist.objects.get(pk=kwargs["pk"])
        serializer = DentistSerializer(
            dentist,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)
        dentist = serializer.save()

        output = DentistListSerializer(dentist, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    @allow_permission([ROLE.ADMIN])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @allow_permission([ROLE.ADMIN])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
