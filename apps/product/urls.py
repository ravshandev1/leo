from django.urls import path
from .views import categories_view, products_view, product_detail_view, order_view, order_confirm_view, confirm_view

urlpatterns = [
    path('', categories_view, name='categories'),
    path('products/<int:cat_id>/', products_view, name='products'),
    path('<int:pk>/', product_detail_view, name='product-detail'),
    path('order/<int:pk>/', order_view, name='order'),
    path('order-confirm/<int:pk>/', order_confirm_view, name='order-confirm'),
    path('confirm/', confirm_view, name='confirm'),
]
