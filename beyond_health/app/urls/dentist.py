from django.urls import path

from beyond_health.app.views.dentist.base import DentistViewSet, DentistRestPasswordEndpoint

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
    path('dentists/reset-password',
         DentistRestPasswordEndpoint.as_view(),
         name='change-password'
         ),

]
