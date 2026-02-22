from beyond_health.app.serializers.base import BaseSerializer
from beyond_health.db.models.notification import UserNotification, Notification


class NotificationListSerializer(BaseSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserNotificationListSerializer(BaseSerializer):
    notification = NotificationListSerializer()

    class Meta:
        model = UserNotification
        fields = '__all__'
