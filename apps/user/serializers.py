from rest_framework import serializers
from .models import Region, TelegramUser, UserPoint, UserPointImage, VerifyPhone, InfoPhone, Info


class InfoPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoPhone
        fields = ['phone']


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ['link', 'phones']

    phones = InfoPhoneSerializer(many=True, read_only=True)


class VerifyPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPhone
        fields = ['phone', 'code']


class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField()


class UserPointImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPointImage
        fields = ['image']


class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint
        fields = ['user', 'bonus', 'images']

    images = UserPointImageSerializer(many=True)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name_uz', 'name_ru']


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['name', 'chat_id', 'phone', 'region', 'lang', 'point']

    point = serializers.IntegerField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['chat_id', 'lang']
