from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers.dental_problem import DentalProblemListSerializer
from beyond_health.db.models import DentalProblem


# Create your views here.
class DentalProblemViewSet(BaseViewSet):
    model = DentalProblem
    serializer_class = DentalProblemListSerializer

    search_fields = ["name"]
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
