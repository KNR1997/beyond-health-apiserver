from django.urls import path

from beyond_health.app.views.shift.base import ShiftViewSet

urlpatterns = [
    path(
        "shifts/",
        ShiftViewSet.as_view({"get": "list"}),
        name="shift",
    ),
]
