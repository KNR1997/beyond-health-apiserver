from django.urls import path

from beyond_health.app.views.notification.base import NotificationViewSet, NotificationReadEndpoint

urlpatterns = [
    path(
        "notifications/",
        NotificationViewSet.as_view({"get": "list"}),
        name="notification",
    ),
    path(
        "notifications/<int:pk>/",
        NotificationViewSet.as_view({
            "get": "retrieve",
        }),
        name="notification",
    ),
    path('notifications/read',
         NotificationReadEndpoint.as_view(),
         name='notification-read'
         ),
]
