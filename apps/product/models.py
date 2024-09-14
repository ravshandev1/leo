from django.db import models
from django.conf import settings
from user.models import Bonus, TelegramUser, Store


class Category(models.Model):
    name = models.CharField(max_length=250)
    icon = models.ImageField(upload_to='categories/')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def icon_url(self):
        return f"{settings.BASE_URL}{self.icon.url}"

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, models.CASCADE, 'sub_categories')

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(SubCategory, models.CASCADE, 'products')
    name = models.CharField(max_length=250, unique=True)
    bonus = models.OneToOneField(Bonus, models.CASCADE, related_name='products',
                                 limit_choices_to={'has_product': False})
    price = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.bonus.has_product is False:
            self.bonus.has_product = True
            self.bonus.save()


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.product.name

    @property
    def image_path(self):
        return f"{settings.BASE_URL}{self.image.url}"


class Order(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'orders')
    product = models.ForeignKey(Product, models.CASCADE, 'orders')
    count = models.IntegerField(default=1)
    total = models.IntegerField(default=1)
    store = models.ForeignKey(Store, models.CASCADE, 'orders')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user


class Cart(models.Model):
    user = models.ForeignKey(TelegramUser, models.CASCADE, 'carts')
    product = models.ForeignKey(Product, models.CASCADE, 'carts')
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.user
