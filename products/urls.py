from django.urls import path
from . import views

urlpatterns = [
    path('products_v2/', views.get_products, name='get_products'),
    path('products_v2/<int:pk>', views.update_product, name='update_product'),
]
