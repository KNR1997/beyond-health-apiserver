from django.urls import path
from rest_framework.routers import DefaultRouter

from user.views.admin import AdminViewSet
from user.views.dentist import DentistViewSet
from user.views.patient import PatientViewSet
from user.views.staff import StaffViewSet
from user.views.user import UserViewSet

router = DefaultRouter()

urlpatterns = [
    path(
        "admin/list/",
        AdminViewSet.as_view({"get": "list"}),
        name="admin",
    ),
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
        "patients/",
        PatientViewSet.as_view({"get": "list", "post": "create"}),
        name="patient",
    ),
    path(
        "patients/<uuid:pk>/",
        PatientViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="patient",
    ),
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
    path(
        "staff/",
        StaffViewSet.as_view({"get": "list", "post": "create"}),
        name="staff",
    ),
    path(
        "staff/<uuid:pk>/",
        StaffViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="dentist",
    ),
]
