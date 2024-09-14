from requests import request
from django.conf import settings
import json


def send_verification_code(phone: str, code: str):
    token = request("post", 'https://notify.eskiz.uz/api/auth/login',
                    data={'email': settings.SMS_EMAIL, 'password': settings.SMS_PASSWORD})
    headers = {
        "Authorization": f"Bearer {token.json()['data']['token']}",
        "Content-Type": "application/json"
    }
    data = {
        'mobile_phone': phone,
        'message': f"Leo Usta Bot ro'yxatdan o'tish uchun tasdiqlash kodi: {code}\nЛео мастер бот код подтверждения регистрации: {code}",
        'from': "4546",
    }
    request("post", 'https://notify.eskiz.uz/api/message/sms/send', data=json.dumps(data), headers=headers)
