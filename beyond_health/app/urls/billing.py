from django.urls import path

from beyond_health.app.views.billing.base import BillingViewSet

urlpatterns = [
    path(
        "billings/",
        BillingViewSet.as_view({"get": "list", "post": "create"}),
        name="billing",
    ),
    path(
        "billings/<uuid:pk>/",
        BillingViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="billing",
    ),
]
