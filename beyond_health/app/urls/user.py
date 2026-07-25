from django.urls import path

from beyond_health.app.views.user.base import UserViewSet
from beyond_health.app.views.user.admin import ResetUserPasswordEndpoint

urlpatterns = [
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user",
    ),
    path(
        "users/<uuid:pk>/",
        UserViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="user",
    ),
    path(
        "admin/users/<uuid:user_id>/reset-password",
        ResetUserPasswordEndpoint.as_view(),
        name="reset-user-password",
    ),
    path(
        "users/block-user",
        UserViewSet.as_view({"post": "block_user"}),
        name="user",
    ),
    path(
        "users/unblock-user",
        UserViewSet.as_view({"post": "unblock_user"}),
        name="user",
    ),
]
