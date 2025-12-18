from django.urls import path

from medical_records.views.problem import ProblemViewSet

urlpatterns = [
    path(
        "dental-problems/",
        ProblemViewSet.as_view({"get": "list", "post": "create"}),
        name="problem",
    ),
    path(
        "dental-problems/<uuid:pk>/",
        ProblemViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="problem",
    ),
]
