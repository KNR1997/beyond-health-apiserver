from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers.shift import ShiftListSerializer
from beyond_health.db.models import Shift


# Create your views here.
class ShiftViewSet(BaseViewSet):
    model = Shift
    serializer_class = ShiftListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
