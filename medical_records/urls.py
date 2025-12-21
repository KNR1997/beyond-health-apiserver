from django.urls import path

from medical_records.views.dental_problem import DentalProblemViewSet
from medical_records.views.patient_dental_problem import PatientDentalProblemViewSet

urlpatterns = [
    path(
        "dental-problems/",
        DentalProblemViewSet.as_view({"get": "list", "post": "create"}),
        name="problem",
    ),
    path(
        "dental-problems/<uuid:pk>/",
        DentalProblemViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="problem",
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
