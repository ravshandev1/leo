from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = 'Регионы'


class Info(models.Model):
    link = models.CharField(max_length=100, verbose_name="Ссылка на телеграмму")

    def __str__(self):
        return self.link

    class Meta:
        verbose_name = "Связаться с нами"
        verbose_name_plural = "Связаться с нами"


class InfoPhone(models.Model):
    info = models.ForeignKey(Info, models.CASCADE, 'phones')
    phone = models.CharField(max_length=100, verbose_name="Телефон")

    def __str__(self):
        return self.phone


class Store(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    region = models.ForeignKey(Region, models.CASCADE, 'stores', verbose_name="Регион")
    longitude = models.CharField(max_length=100)
    latitude = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.region}, {self.name}"

    class Meta:
        verbose_name_plural = 'Магазины'
        verbose_name = 'Магазин'


class StorePhone(models.Model):
    phone = models.CharField(max_length=100, verbose_name="Телефон магазина")
    store = models.ForeignKey(Store, models.CASCADE, 'phones')

    def __str__(self):
        return self.phone


class TelegramUser(models.Model):
    name = models.CharField(max_length=120, verbose_name="Имя")
    chat_id = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=100, verbose_name="Телефон")
    region = models.ForeignKey(Region, models.SET_NULL, null=True, blank=True, verbose_name="Регион")
    lang = models.CharField(max_length=2, verbose_name="Язык")
    summa = models.IntegerField(default=0, verbose_name="Сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Созданный на")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class VerifyPhone(models.Model):
    phone = models.CharField(max_length=100, verbose_name="Телефон")
    code = models.CharField(max_length=5, verbose_name="Код")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Созданный на")

    def __str__(self):
        return self.phone
