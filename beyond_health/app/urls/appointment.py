from django.urls import path

from beyond_health.app.views.appointment.base import AppointmentViewSet

urlpatterns = [
    path(
        "appointments/",
        AppointmentViewSet.as_view({"get": "list", "post": "create"}),
        name="Appointment",
    ),
    path(
        "appointments/<uuid:pk>/",
        AppointmentViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            # "patch": "partial_update",
            # "delete": "destroy",
        }),
        name="appointment",
    ),
]
