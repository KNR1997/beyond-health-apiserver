from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.serializers.treatment import TreatmentPlanItemListSerializer, TreatmentPlanItemsCreateSerializer
from beyond_health.app.views.base import BaseViewSet
from beyond_health.db.models import TreatmentPlanItem


# Create your views here.
class TreatmentPlanItemViewSet(BaseViewSet):
    model = TreatmentPlanItem
    serializer_class = TreatmentPlanItemListSerializer

    search_fields = ["name"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = TreatmentPlanItemsCreateSerializer(
            data={**request.data}
        )
        if serializer.is_valid():
            serializer.save()

            return Response(None, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = TreatmentPlanItemsCreateSerializer(
            data={**request.data}
        )

        if serializer.is_valid():
            serializer.update(None, serializer.validated_data)
            return Response(None, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        treatment_plan_id = kwargs.get('pk')

        plan_items = TreatmentPlanItem.objects.filter(treatment_plan_id=treatment_plan_id)
        serializer = TreatmentPlanItemListSerializer(plan_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
