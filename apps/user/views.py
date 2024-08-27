from rest_framework import generics, response
from .serializers import RegionSerializer, TelegramUserSerializer, UserSerializer, UserPointSerializer, PhoneSerializer, \
    VerifyPhoneSerializer, InfoSerializer
from .models import TelegramUser, Region, Bonus, UserPoint, VerifyPhone, Info
from .utils import send_verification_code
from random import randint


class RegionListView(generics.ListAPIView):
    serializer_class = RegionSerializer
    queryset = Region.objects.all()


class InfoView(generics.GenericAPIView):
    serializer_class = InfoSerializer

    def get(self, request, *args, **kwargs):
        obj = Info.objects.first()
        serializer = InfoSerializer(obj)
        return response.Response(serializer.data)


class CheckCodeView(generics.GenericAPIView):
    serializer_class = UserPointSerializer

    def get(self, request, *args, **kwargs):
        if not Bonus.objects.filter(code=kwargs['code']).first():
            return response.Response({"success": False, "message_uz": "Bunday code mavjud emas!", "message_ru": ""},
                                     status=404)
        if UserPoint.objects.exists(bonus__code=kwargs['code']):
            return response.Response({"success": False, "message_uz": "Bu code avval foydalanilgan", "message_ru": ""},
                                     status=404)
        return response.Response({"success": True})

    def post(self, request, *args, **kwargs):
        user = TelegramUser.objects.filter(chat_id=self.request.data['user']).first()
        bonus = Bonus.objects.get(code=kwargs['code'])
        self.request.data['user'] = user.id
        self.request.data['bonus'] = bonus.id
        serializer = UserPointSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"success": True,
                                  "message_uz": f"Hisobingizga {bonus.point} ball qo'shildi!\nBu ball 1 yil davomida amal qiladi\nAgar balldan foydalanmasangiz 1 yildan so'ng o'chib ketadi!",
                                  "message_ru": ""})


class SendCodeView(generics.GenericAPIView):
    serializer_class = PhoneSerializer

    def post(self, request, *args, **kwargs):
        code = str(randint(10000, 99999))
        code = "77777"
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
        obj = TelegramUser.objects.filter(chat_id=kwargs['chat_id']).first()
        if not obj:
            return response.Response({"success": False, "message": "User not found!"}, status=404)
        return response.Response({"success": True, "message": "User found!"})


class TelegramUserView(generics.GenericAPIView):
    serializer_class = TelegramUserSerializer

    def get(self, request, *args, **kwargs):
        obj = TelegramUser.objects.filter(chat_id=kwargs['chat_id']).first()
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
        serializer = TelegramUserSerializer(instance=obj, data=self.request.data)
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
