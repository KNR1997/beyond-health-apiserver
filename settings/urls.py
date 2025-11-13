from django.urls import path

from settings.views import SettingsViewSet

urlpatterns = [
    path('settings/', SettingsViewSet.as_view(), name="settings"),
]
