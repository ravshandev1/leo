from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, models.CASCADE, 'stores')
    image = models.ImageField(upload_to='stores/')
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.name


class StorePhone(models.Model):
    phone = models.CharField(max_length=12)
    store = models.ForeignKey(Store, models.CASCADE, 'phones')

    def __str__(self):
        return self.phone


class TelegramUser(models.Model):
    name = models.CharField(max_length=120)
    chat_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=13)
    region = models.ForeignKey(Region, models.SET_NULL, null=True, blank=True)
    lang = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def point(self):
        return sum([i.bonus.point for i in self.points.filter(is_active=True)])


class VerifyPhone(models.Model):
    phone = models.CharField(max_length=13)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone


class Bonus(models.Model):
    code = models.CharField(max_length=10, unique=True)
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
        return self.user


class UserPointImage(models.Model):
    point = models.ForeignKey(UserPoint, models.CASCADE, 'images')
    image = models.ImageField(upload_to='user_points')

    def __str__(self):
        return self.point
