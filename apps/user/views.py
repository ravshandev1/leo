from celery import shared_task
from rest_framework import generics, response
from .serializers import RegionSerializer, TelegramUserSerializer, UserSerializer, PhoneSerializer, \
    VerifyPhoneSerializer, InfoSerializer, StoreSerializer
from .models import TelegramUser, Region, VerifyPhone, Info, Store
from product.models import Bonus, UserSumma
from .utils import send_verification_code
from random import randint
import re


class StoreListView(generics.ListAPIView):
    serializer_class = StoreSerializer

    def get_queryset(self):
        user = TelegramUser.objects.filter(chat_id=self.kwargs['chat_id']).first()
        return Store.objects.filter(region_id=user.region_id)


class RegionListView(generics.ListAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


@shared_task
def dl():
    bonuses = Bonus.objects.all()
    ls = list()
    pattern = r'(\d{4})\D*$'
    for bonus in bonuses:
        match = re.search(pattern, bonus.code).group(1)
        if match:
            number = int(match)
            if 1 <= number <= 9999:
                print(f"Deleting bonus code: {bonus.code}")
                ls.append(bonus.id)
    Bonus.objects.filter(id__in=ls).delete()
    return "Done"


class InfoView(generics.GenericAPIView):
    serializer_class = InfoSerializer

    def get(self, request, *args, **kwargs):
        obj = Info.objects.first()
        serializer = self.serializer_class(obj)
        return response.Response(serializer.data)


class CheckCodeView(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    def get(self, request, *args, **kwargs):
        if UserSumma.objects.filter(code=kwargs['code']).first():
            return response.Response({"success": False, "message_uz": "Bu code avval foydalanilgan!",
                                      "message_ru": "Этот код использовался ранее!"},
                                     status=404)
        code = self.kwargs['code']
        number = re.search(r'(\d{4})\D*$', code).group(1)
        if 0000 >= int(number) >= 9999:
            return response.Response({"success": False, "message_uz": "Bunday code mavjud emas!",
                                      "message_ru": "Такого кода не существует!"},
                                     status=404)
        code = code.replace(number, "0000")
        if not Bonus.objects.filter(code=code).exists():
            return response.Response({"success": False, "message_uz": "Bunday code mavjud emas!",
                                      "message_ru": "Такого кода не существует!"},
                                     status=404)

        return response.Response({"success": True})

    def post(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(chat_id=self.request.data['chat_id']).first()
        code = self.kwargs['code']
        number = re.search(r'(\d{4})\D*$', code).group(1)
        code = code.replace(number, "0000")
        bonus = Bonus.objects.filter(code=code).first()
        if bonus:
            user.summa += bonus.summa
            user.save()
            UserSumma.objects.create(user_id=user.id, code=code)
            return response.Response({"success": True,
                                      "message_uz": f"Hisobingizga {bonus.summa} so'm qo'shildi!\nBu so'm 1 yil davomida amal qiladi\nAgar so'mdan foydalanmasangiz 1 yildan so'ng o'chib ketadi!",
                                      "message_ru": f"{bonus.summa} сум добавлены к вашему счету!\n этот сум действителен в течение 1 года\nесли вы не используете сум, он исчезнет через 1 год!"})
        return response.Response(
            {"success": False, "message_uz": "Bonus code mavjud emas", "message_ru": "Бонусный код недоступен"},
            status=404)


class SendCodeView(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        code = str(randint(10000, 99999))
        phone = self.request.data['phone']
        send_verification_code(phone, code)
        VerifyPhone.objects.create(phone=phone, code=code)
        return response.Response({"success": True})


class VerifyCodeView(generics.GenericAPIView):
    serializer_class = VerifyPhoneSerializer

    def post(self, request, *args, **kwargs):
        phone = self.request.data['phone']
        code = self.request.data['code']
        obj = VerifyPhone.objects.filter(phone=phone, code=code).first()
        if obj:
            obj.delete()
            return response.Response({"success": True})
        return response.Response(
            {"success": False, "message_uz": "Tasdiqlash code xato", "message_ru": "Ошибка кода подтверждения"},
            status=400)


class UserCheckView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        obj = TelegramUser.objects.filter(chat_id=self.kwargs['chat_id']).first()
        if not obj:
            return response.Response({"success": False, "message": "User not found!"}, status=404)
        return response.Response({"success": True, "message": "User found!"})


class TelegramUserView(generics.GenericAPIView):
    serializer_class = TelegramUserSerializer

    def get(self, request, *args, **kwargs):
        obj = TelegramUser.objects.filter(chat_id=self.kwargs['chat_id']).first()
        if not obj:
            return response.Response({'success': False, 'message': 'User not found!'}, status=404)
        serializer = TelegramUserSerializer(obj).data
        region = Region.objects.get(id=serializer['region'])
        serializer.update({'region': region.name})
        return response.Response(serializer)

    def patch(self, request, *args, **kwargs):
        obj = TelegramUser.objects.filter(chat_id=kwargs['chat_id']).first()
        if not obj:
            return response.Response({'success': False, 'message': 'User not found!'}, status=404)
        serializer = TelegramUserSerializer(instance=obj, data=self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = TelegramUserSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = TelegramUser.objects.all()
