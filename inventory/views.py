from core.views.base import BaseViewSet
from inventory.models import Inventory
from inventory.serializers import InventoryListSerializer
from treatments.models import Treatment
from treatments.serializers import TreatmentListSerializer


# Create your views here.
class InventoryViewSet(BaseViewSet):
    model = Inventory
    serializer_class = InventoryListSerializer

    search_fields = ["item_name"]
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
