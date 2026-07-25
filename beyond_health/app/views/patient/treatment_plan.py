from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet
from beyond_health.db.models import TreatmentPlan
from beyond_health.app.serializers.treatment import TreatmentPlanListSerializer


class PatientTreatmentPlanViewSet(BaseViewSet):
    model = TreatmentPlan
    serializer_class = TreatmentPlanListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def get_queryset(self):
        patient_id = self.kwargs.get("pk")
        return self.filter_queryset(
            super().get_queryset().filter(patient_id=patient_id)
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
