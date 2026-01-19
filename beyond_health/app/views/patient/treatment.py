from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet, BaseAPIView
from beyond_health.app.serializers.patient import PatientProblemBulkCreateSerializer
from beyond_health.app.serializers.treatment import TreatmentListSerializer
from beyond_health.db.models import Treatment, Patient


# Create your views here.
class TreatmentViewSet(BaseViewSet):
    model = Treatment
    serializer_class = TreatmentListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def create(self, request, *args, **kwargs):
        serializer = PatientProblemBulkCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient_problems = serializer.save()

        output = TreatmentListSerializer(
            patient_problems,
            many=True
        ).data

        return Response(output, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        patient_id = kwargs.get("pk")

        patient = get_object_or_404(Patient, pk=patient_id)

        patient_problems = (
            Treatment.objects
            .filter(patient=patient)
            .select_related("problem")
        )

        serializer = self.get_serializer(
            patient_problems,
            many=True
        )

        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientTreatmentStatusChangeEndpoint(BaseAPIView):
    def post(self, request):
        treatment_id = request.data["id"]
        treatment = get_object_or_404(Treatment, pk=treatment_id)

        if treatment.is_active:
            treatment.is_active = False
        else:
            treatment.is_active = True

        treatment.save()
        serializer = TreatmentListSerializer(treatment)
        return Response(serializer.data, status=status.HTTP_200_OK)
