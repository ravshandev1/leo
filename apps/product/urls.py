from django.urls import path
from .views import CategoryListView, ProductListView, ProductDetailView, CartListView, OrderView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/<int:subcategory_id>/<int:chat_id>/', ProductListView.as_view(), name='products'),
    path('<int:pk>/<int:chat_id>/', ProductDetailView.as_view(), name='product-detail'),
    path('my-cart/<int:chat_id>/', CartListView.as_view(), name='cart'),
    path('order/<int:chat_id>/', OrderView.as_view(), name='order')
]
