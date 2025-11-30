from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet

from user.models import Dentist
from user.serializers import DentistListSerializer, DentistCreateSerializer


# Create your views here.
class DentistViewSet(BaseViewSet):
    model = Dentist
    serializer_class = DentistListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        serializer = DentistCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = serializer.save()

        output = DentistCreateSerializer(patient, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
