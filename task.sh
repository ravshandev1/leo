#!/bin/bash
cd /home/ravshan/Projects/leo
source .venv/bin/activate
echo "
import datetime
from django.utils import timezone
from django.conf import settings
import requests
from user.models import UserPoint

TELEGRAM_API_URL = f'https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage'

def send_telegram_message(chat_id, message):
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(TELEGRAM_API_URL, data=payload)
    return response.status_code == 200

def process_user_points():
    one_year_ago = timezone.now() - datetime.timedelta(days=365)
    one_week_left = timezone.now() - datetime.timedelta(days=365 - 7)

    expired_points = UserPoint.objects.filter(created_at__lte=one_year_ago)
    for point in expired_points:
        point.user.summa -= point.bonus.summa
        point.user.save()

    points_soon_to_expire = UserPoint.objects.filter(created_at__range=[one_week_left, one_year_ago])
    for point in points_soon_to_expire:
        message_uz = 'Balingizni foydalaning, yuqsa 1 haftadan keyin o\'chib ketadi.'
        message_ru = 'Balingizni foydalaning, yuqsa 1 haftadan keyin o\'chib ketadi.'
        if point.user.lang == 'uz':
            message = message_uz
        else:
            message = message_ru
        send_telegram_message(point.user.chat_id, message)
process_user_points()
" | python manage.py shell

