from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.serializers.treatment import TreatmentPlanListSerializer, TreatmentPlanSerializer
from beyond_health.app.views.base import BaseViewSet
from beyond_health.db.models import TreatmentPlan, Patient


# Create your views here.
class TreatmentPlanViewSet(BaseViewSet):
    model = TreatmentPlan
    serializer_class = TreatmentPlanListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            serializer = TreatmentPlanSerializer(
                data={**request.data}
            )
            if serializer.is_valid():
                serializer.save()

                treatment_plan = self.get_queryset().filter(pk=serializer.data["id"]).first()

                serializer = TreatmentPlanListSerializer(treatment_plan)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as e:
            if "already exists" in str(e):
                return Response(
                    {"name": "The project name is already taken"},
                    status=status.HTTP_409_CONFLICT,
                )
        except Patient.DoesNotExist:
            return Response(
                {"error": "patient does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
