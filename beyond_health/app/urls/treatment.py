from django.urls import path

from beyond_health.app.views.patient.treatment import PatientTreatmentStatusChangeEndpoint
from beyond_health.app.views.treatment.base import TreatmentViewSet

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
    path(
        "treatment-status-change",
        PatientTreatmentStatusChangeEndpoint.as_view(),
        name="patient-treatment-change",
    ),
]
