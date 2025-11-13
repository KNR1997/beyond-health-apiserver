from django.urls import path
from rest_framework.routers import DefaultRouter

from treatments.views import TreatmentViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        "treatments/",
        TreatmentViewSet.as_view({"get": "list", "post": "create"}),
        name="treatment",
    ),
    path(
        "treatments/<uuid:pk>/",
        TreatmentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="treatment",
    ),
]
