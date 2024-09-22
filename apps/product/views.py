from pytz import timezone
from .models import Category, Product, Cart
from user.models import TelegramUser
from requests import post
from django.conf import settings
from rest_framework import generics, response
from .serializers import ProductSerializer, CategorySerializer, CartSerializer, OrderSerializer, OrderProductSerializer


class OrderView(generics.GenericAPIView):
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(chat_id=self.kwargs['chat_id']).first()
        if not user:
            return response.Response({'error': 'User not found'}, status=404)
        data = self.request.data
        data['user'] = user.id
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        user.summa -= order.total
        user.save()
        products_uz = ""
        phones = ""
        for i in order.store.phones.all():
            phones += f"{i.phone}\n"
        products_ru = ""
        for i in order.products.all():
            products_uz += f"Nomi: {i.product.name_uz}\nSoni: {i.count}\nNarxi: {i.product.price} so'm\n"
            products_ru += f"Продукт: {i.product.name_ru}\nКоличество: {i.count}\nСтоимость: {i.product.price}Сум\n"
        txt = f"Foydalanuvchi: {user.phone}\nViloyat: {order.store.region.name_uz}\nMahsulotlar: \n{products_uz}"
        txt += f"Dukon: {order.store.name_uz}\nBuyurtma vaqti: {order.created_at.astimezone(tz=timezone('Asia/Tashkent')).strftime('%d-%m-%Y %H:%M')}"
        payload = {
            "chat_id": settings.GROUP_ID,
            "text": txt,
            "parse_mode": "HTML"
        }
        telegram_response = post(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage", json=payload)
        if telegram_response.status_code != 200:
            return response.Response({'error': 'Failed to send message to Telegram'}, status=500)
        if user.lang == "uz":
            txt = f"Mahsulotlar: \n{products_uz}Dukon nomi: {order.store.name_uz}\nViloyat: {order.store.region.name_uz}\nJami: {order.total} so'm\n5 kundan so'ng olishingiz mumkin\nTelefonlar: {phones}\n"
        elif user.lang == "ru":
            txt = f"Продукты: \n{products_ru}Название магазина: {order.store.name_ru}\nРегион: {order.store.region.name_ru}\nВы можете получить его через 5 дней\nИтого: {order.total} Сум\nТелефоны: {phones}\n"

        payload = {
            "chat_id": user.chat_id,
            "text": txt,
            "parse_mode": "HTML"
        }
        post(f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage", json=payload)
        user.carts.all().delete()
        return response.Response({'success': True})


class CategoryListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductListView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(chat_id=self.kwargs['chat_id']).first()
        data = list()

        for i in Product.objects.filter(category_id=self.kwargs['subcategory_id']):
            d = ProductSerializer(i).data
            if Cart.objects.filter(product_id=i, user_id=user.id).exists():
                d['has_in_cart'] = True
            d['has_in_cart'] = False
            data.append(d)
        return response.Response(data)


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CartSerializer
        return OrderProductSerializer

    def get_queryset(self):
        return Cart.objects.filter(user__chat_id=self.kwargs['chat_id'])

    def post(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(chat_id=self.kwargs['chat_id']).first()
        Cart.objects.create(user_id=user.id, product_id=self.request.data['product'],
                            count=int(self.request.data['count']))
        return response.Response({'success': True})
