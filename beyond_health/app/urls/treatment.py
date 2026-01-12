from django.urls import path

from beyond_health.app.views.treatment.base import TreatmentViewSet
from beyond_health.app.views.treatment.plan import TreatmentPlanViewSet
from beyond_health.app.views.treatment.plan_item import TreatmentPlanItemViewSet

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
        name="treatments",
    ),

    path(
        "treatment-plans/",
        TreatmentPlanViewSet.as_view({"get": "list", "post": "create"}),
        name="treatment-plan",
    ),
    path(
        "treatment-plans/<uuid:pk>/",
        TreatmentPlanViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="treatment-plan",
    ),

    path(
        "treatment-plans/<uuid:treatment_plan_id>/items/",
        TreatmentPlanItemViewSet.as_view({"get": "list", "post": "create"}),
        name="treatments-plan-item",
    ),
]
