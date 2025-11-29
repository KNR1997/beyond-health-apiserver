from django.urls import path
from rest_framework.routers import DefaultRouter

from appointments.views import AppointmentViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        "appointments/",
        AppointmentViewSet.as_view({"get": "list", "post": "create"}),
        name="appointment",
    ),
    path(
        "appointments/<uuid:pk>/",
        AppointmentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="appointment",
    ),
]
