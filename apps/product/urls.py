from django.urls import path
from .views import categories_view, products_view, product_detail_view, order_view

urlpatterns = [
    path('', categories_view, name='categories'),
    path('products/<int:cat_id>/', products_view, name='products'),
    path('<int:pk>/', product_detail_view, name='product-detail'),
    path('order/<int:pk>/', order_view, name='order'),
]
