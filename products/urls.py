from django.urls import path

from . import views

urlpatterns = [
    path('products_v2/', views.get_products, name='get_products'),
    path('products_v2/<int:pk>', views.update_product, name='update_product'),
    path('products_v2/<slug:slug>', views.get_product_by_slug, name="get_product_by_slug"),
    path('products_v2/<int:pk>/delete', views.delete_product, name="delete_product"),
]
