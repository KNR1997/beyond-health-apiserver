from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts import views
from products.views import get_products

router = DefaultRouter()
router.register("user", views.UserViewSet, basename="user")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djoser.urls')),
    path('api/', include('djoser.urls.jwt')),

    path('api-auth/', include('rest_framework.urls')),

    path('api/', include('products.urls')),
]

urlpatterns += router.urls
