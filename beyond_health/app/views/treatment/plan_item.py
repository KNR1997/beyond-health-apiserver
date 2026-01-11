from beyond_health.app.serializers.treatment import TreatmentPlanItemListSerializer
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
        return super().create(request, *args, **kwargs)
