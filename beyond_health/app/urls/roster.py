from django.urls import path

from beyond_health.app.views.roster.assignment import RosterAssignmentViewSet
from beyond_health.app.views.roster.base import RosterWeekViewSet

urlpatterns = [
    path(
        "roster-weeks/",
        RosterWeekViewSet.as_view({"get": "list", "post": "create"}),
        name="roster-week",
    ),
    path(
        "roster-weeks/<uuid:pk>/",
        RosterWeekViewSet.as_view({
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }),
        name="roster-week",
    ),

    path(
        "roster-assignments/<int:pk>/",
        RosterAssignmentViewSet.as_view({"delete": "destroy"}),
        name="roster-assignments",
    ),

    path(
        "roster-weeks/<uuid:pk>/assignments",
        RosterAssignmentViewSet.as_view({
            "get": "list",
            "post": "create",
        }),
        name="roster-week-assignments",
    ),

]
