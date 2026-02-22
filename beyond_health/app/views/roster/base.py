from django.shortcuts import get_object_or_404

from beyond_health.app.base import BaseViewSet
from beyond_health.app.serializers.roster import RosterWeekListSerializer
from beyond_health.db.models.notification import Notification, UserNotification
from beyond_health.db.models.roster import RosterWeek, RosterAssignment


# Create your views here.
class RosterWeekViewSet(BaseViewSet):
    model = RosterWeek
    serializer_class = RosterWeekListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        return (
            self.filter_queryset(super().get_queryset())
        )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        status = request.data["status"]
        roster_week = get_object_or_404(RosterWeek, pk=kwargs.get("pk"))

        if roster_week.status == RosterWeek.Status.DRAFT and status == RosterWeek.Status.PUBLISHED:
            assignments = RosterAssignment.objects.filter(roster_week=roster_week)
            users = assignments.values_list('user', flat=True).distinct()

            notification = Notification.objects.create(
                title="Roster Published",
                message=f"Your roster for week {roster_week.week_start_date} is published. Please check your schedule.",
                type="ROSTER_PUBLISHED",
                priority="medium",
            )

            UserNotification.objects.bulk_create([
                UserNotification(notification=notification, user_id=user_id)
                for user_id in users
            ])

        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
