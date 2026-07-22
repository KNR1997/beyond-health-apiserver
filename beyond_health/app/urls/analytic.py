from django.urls import path

from beyond_health.app.views.analytic.base import AnalyticsDataEndpoint

urlpatterns = [
    path(
        "analytics/",
        AnalyticsDataEndpoint.as_view(),
        name="analytics-data",
    ),
]