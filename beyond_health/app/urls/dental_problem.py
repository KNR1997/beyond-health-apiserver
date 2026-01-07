from django.urls import path

from beyond_health.app.views.dental_problem.base import DentalProblemViewSet
from beyond_health.app.views.patient.dental_problem import PatientDentalProblemStatusChangeEndpoint

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
        "dental-problem-status-change",
        PatientDentalProblemStatusChangeEndpoint.as_view(),
        name="patient-dental-status-change",
    ),
]
