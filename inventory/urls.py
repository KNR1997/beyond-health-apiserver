from django.urls import path
from rest_framework.routers import DefaultRouter

from inventory.views import InventoryViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        "inventory/",
        InventoryViewSet.as_view({"get": "list", "post": "create"}),
        name="inventory",
    ),
    path(
        "inventory/<uuid:pk>/",
        InventoryViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="inventory",
    ),
]
