from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from core.views.base import BaseViewSet
from medical_records.models import PatientProblem
from medical_records.serializers import PatientProblemListSerializer, PatientProblemBulkCreateSerializer
from user.models import Patient


# Create your views here.
class PatientDentalProblemViewSet(BaseViewSet):
    model = PatientProblem
    serializer_class = PatientProblemListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def create(self, request, *args, **kwargs):
        serializer = PatientProblemBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient_problems = serializer.save()

        output = PatientProblemListSerializer(
            patient_problems,
            many=True
        ).data

        return Response(output, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        patient_id = kwargs.get("pk")

        patient = get_object_or_404(Patient, pk=patient_id)

        patient_problems = (
            PatientProblem.objects
            .filter(patient=patient)
            .select_related("problem")
        )

        serializer = self.get_serializer(
            patient_problems,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
