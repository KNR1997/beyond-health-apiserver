from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from beyond_health.app.base import BaseViewSet, BaseAPIView
from beyond_health.app.serializers.notification import UserNotificationListSerializer
from beyond_health.db.models.notification import UserNotification


# Create your views here.
class NotificationViewSet(BaseViewSet):
    model = UserNotification
    serializer_class = UserNotificationListSerializer

    search_fields = []
    filterset_fields = []

    def get_queryset(self):
        user = self.request.user
        return (
            self.filter_queryset(super().get_queryset().filter(user=user))
        )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class NotificationReadEndpoint(BaseAPIView):
    def post(self, request):
        user_notification_id = request.data["id"]
        user_notification = get_object_or_404(UserNotification, pk=user_notification_id)

        user_notification.is_read = True
        user_notification.save()

        return Response(status=status.HTTP_200_OK)
