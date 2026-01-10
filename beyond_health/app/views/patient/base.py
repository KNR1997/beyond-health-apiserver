from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers.patient import PatientSerializer, PatientListSerializer
from beyond_health.db.models import Patient


# Create your views here.
class PatientViewSet(BaseViewSet):
    model = Patient
    serializer_class = PatientListSerializer

    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = serializer.save()

        output = PatientListSerializer(patient, context={"request": request}).data
        return Response(output, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        patient = Patient.objects.get(pk=kwargs["pk"])

        serializer = PatientSerializer(
            patient,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        output = PatientListSerializer(patient, context={"request": request}).data
        return Response(output, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
