from django.urls import path

from beyond_health.app.views.patient.base import PatientViewSet
from beyond_health.app.views.patient.dental_problem import PatientDentalProblemViewSet

urlpatterns = [
    path(
        "patients/",
        PatientViewSet.as_view({"get": "list", "post": "create"}),
        name="patient",
    ),
    path(
        "patients/<uuid:pk>/",
        PatientViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="patient",
    ),

    path(
        "patient-dental-problems/",
        PatientDentalProblemViewSet.as_view({"post": "create"}),
        name="patient-dental-problem",
    ),

    path(
        "patients/<uuid:pk>/dental-problems/",
        PatientDentalProblemViewSet.as_view({"get": "retrieve", "put": "update"}),
        name="patient-dental-problem",
    )
]
