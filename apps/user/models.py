from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Info(models.Model):
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.link


class InfoPhone(models.Model):
    info = models.ForeignKey(Info, models.CASCADE, 'phones')
    phone = models.CharField(max_length=100)

    def __str__(self):
        return self.phone


class Store(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, models.CASCADE, 'stores')
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class StorePhone(models.Model):
    phone = models.CharField(max_length=100)
    store = models.ForeignKey(Store, models.CASCADE, 'phones')

    def __str__(self):
        return self.phone


class TelegramUser(models.Model):
    name = models.CharField(max_length=120)
    chat_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=100)
    region = models.ForeignKey(Region, models.SET_NULL, null=True, blank=True)
    lang = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def point(self):
        return sum([i.bonus.point for i in self.points.filter(is_active=True)])


class VerifyPhone(models.Model):
    phone = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Bonus(models.Model):
    code = models.CharField(max_length=100, unique=True)
    point = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class UserPoint(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'points')
    bonus = models.ForeignKey(Bonus, models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'self.user'

