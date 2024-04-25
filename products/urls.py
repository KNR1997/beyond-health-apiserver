from django.urls import path

from .views import product_views, type_views, category_views

urlpatterns = [
    path('products_v2/', product_views.get_products, name='get_products'),
    path('products_v2/create', product_views.create_product, name='create_product'),
    path('products_v2/<int:pk>', product_views.update_product, name='update_product'),
    path('products_v2/<slug:slug>', product_views.get_product_by_slug, name="get_product_by_slug"),
    path('products_v2/<int:pk>/delete', product_views.delete_product, name="delete_product"),

    path('types_v2/', type_views.get_types, name='get_types'),

    path('categories_v2/', category_views.get_categories, name='get_categories'),

]
