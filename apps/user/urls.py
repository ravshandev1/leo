from django.urls import path
from .views import RegionListView, UserListView, TelegramUserView, CheckCodeView, SendCodeView, VerifyCodeView, \
    UserCheckView, StoreListView

urlpatterns = [
    path('<int:chat_id>/', TelegramUserView.as_view(), name='telegram_user'),
    path('regions/', RegionListView.as_view(), name='regions'),
    path('check/<int:chat_id>/', UserCheckView.as_view(), name='users'),
    path('users/', UserListView.as_view(), name='users'),
    path('check/<str:code>/', CheckCodeView.as_view(), name='check'),
    path('send-sms/', SendCodeView.as_view(), name='check'),
    path('verify/', VerifyCodeView.as_view(), name='check'),
    path('stores/<int:chat_id>/', StoreListView.as_view(), name='stores'),
]
