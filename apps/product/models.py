from django.db import models
from django.conf import settings
from user.models import Bonus, TelegramUser, Store
from django import forms


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
    category = models.ForeignKey(Category, models.CASCADE, 'sub_categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(SubCategory, models.CASCADE, 'products', verbose_name="Категория")
    name = models.CharField(max_length=250, unique=True, verbose_name="Имя")
    bonus = models.OneToOneField(Bonus, models.CASCADE, related_name='products', verbose_name="Бонус")
    price = models.IntegerField(verbose_name="Цена")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'bonus', 'price', 'description']

    def __init__(self, *args, **kwargs):
        # self.fields['bonus'].queryset = Bonus.objects.filter(has_product=False)
        super().__init__(*args, **kwargs)
        # self.fields['bonus'].queryset = Bonus.objects.filter(has_product=False)

        if 'bonus' in self.fields:
            if self.instance and self.instance.pk:
        #         # Agar yangilanayotgan bo'lsa, bonusni readonly qiling
                self.fields['bonus'].widget.attrs['readonly'] = True
            else:
        #         # Agar mahsulot yaratilayotgan bo'lsa, bonus querysetini filtrlang
                self.fields['bonus'].queryset = Bonus.objects.filter(has_product=False)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.product.name

    @property
    def image_path(self):
        return f"{settings.BASE_URL}{self.image.url}"


class Order(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'orders', verbose_name="Пользователь")
    product = models.ForeignKey(Product, models.CASCADE, 'orders', verbose_name="Продукт")
    count = models.IntegerField(default=1, verbose_name="Количество")
    total = models.IntegerField(default=1, verbose_name="общая сумма")
    store = models.ForeignKey(Store, models.CASCADE, 'orders', verbose_name="Магазин")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Созданный на")

    def __str__(self):
        return self.user
    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'carts')
    product = models.ForeignKey(Product, models.CASCADE, 'carts')
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.user
