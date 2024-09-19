from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, CartListView, OrderView, categories_view, \
    products_view, product_detail_view, order_view, order_confirm_view, confirm_view

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/<int:subcategory_id>/', ProductListView.as_view(), name='products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-cart/<int:chat_id>/', CartListView.as_view(), name='cart'),
    path('order/<int:chat_id>/', OrderView.as_view(), name='order'),
    path('', categories_view, name='categories'),
    path('pr/<int:cat_id>', products_view, name='categories'),
    path('pr-de/<int:pk>', product_detail_view, name='categories'),
]
