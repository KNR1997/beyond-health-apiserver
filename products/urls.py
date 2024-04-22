from django.urls import path
from . import views

urlpatterns = [
    path('products_v2/', views.get_products, name='get_products'),
]
