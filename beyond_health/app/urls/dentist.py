from django.urls import path

from beyond_health.app.views.dentist.base import DentistViewSet

urlpatterns = [
    path(
        "dentists/",
        DentistViewSet.as_view({"get": "list", "post": "create"}),
        name="dentist",
    ),
    path(
        "dentists/<uuid:pk>/",
        DentistViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="dentist",
    ),
]
