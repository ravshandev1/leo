from django.db import models
from django.conf import settings
from user.models import TelegramUser, Store
from celery import shared_task
from time import sleep


class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя")
    icon = models.ImageField(upload_to='categories/')

    @property
    def icon_url(self):
        return f"{settings.BASE_URL}{self.icon.url}"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class SubCategory(models.Model):
    name = models.CharField(max_length=250, verbose_name="Имя")
    parent = models.ForeignKey('self', models.CASCADE, 'children', null=True, blank=True,
                               limit_choices_to={'parent': None})
    icon = models.ImageField(upload_to='subcategories/', null=True, blank=True)
    category = models.ForeignKey(Category, models.CASCADE, 'sub_categories')

    def __str__(self):
        return self.name_ru

    @property
    def icon_url(self):
        return f"{settings.BASE_URL}{self.icon.url}" if self.icon else None


class Product(models.Model):
    category = models.ForeignKey(SubCategory, models.CASCADE, 'products', verbose_name="Категория")
    name = models.CharField(max_length=250, verbose_name="Имя")
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Bonus(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, 'bonuses')
    code = models.CharField(max_length=100, unique=True, verbose_name="Код")
    summa = models.IntegerField(default=1, verbose_name="Сумма")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = 'Бонус'
        verbose_name_plural = 'Бонус'

    def save(self, *args, **kwargs):
        if not Bonus.objects.filter(id=self.pk).exists():
            generate_bonuses.delay(self.pk)
        super().save()

@shared_task
def generate_bonuses(pk: int):
    sleep(10)
    bonus = Bonus.objects.get(pk=pk)
    prefix = bonus.code[:-4]
    for i in range(1, 10000):
        code = f"{prefix}{str(i).zfill(4)}"
        Bonus.objects.create(code=code, product_id=bonus.product.id, summa=bonus.summa)
    return "The Bonuses have created!"

class UserSumma(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'points')
    bonus = models.ForeignKey(Bonus, models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


# class ProductAdminForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = ['category', 'name', 'bonus', 'price', 'description']
#
#     def __init__(self, *args, **kwargs):
#         # self.fields['bonus'].queryset = Bonus.objects.filter(has_product=False)
#         super().__init__(*args, **kwargs)
#         # self.fields['bonus'].queryset = Bonus.objects.filter(has_product=False)
#
#         if 'bonus' in self.fields:
#             if self.instance and self.instance.pk:
#                 self.fields['bonus'].widget.attrs['readonly'] = True
#             else:
#                 self.fields['bonus'].queryset = Bonus.objects.filter(has_product=False)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.product.name

    @property
    def image_url(self):
        return f"{settings.BASE_URL}{self.image.url}"


class Order(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'orders', verbose_name="Пользователь")
    total = models.IntegerField(default=1, verbose_name="общая сумма")
    store = models.ForeignKey(Store, models.CASCADE, 'orders', verbose_name="Магазин")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Созданный на")

    def __str__(self):
        return self.user

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, models.CASCADE, 'products')
    product = models.ForeignKey(Product, models.CASCADE, 'orders', verbose_name="Продукт")
    count = models.IntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'carts')
    product = models.ForeignKey(Product, models.CASCADE, 'carts')
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.user
