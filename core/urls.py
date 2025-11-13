from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('settings.urls')),
    path('api/', include('authentication.urls')),
    path('api/', include('user.urls')),
    path('api/', include('appointments.urls')),
]
