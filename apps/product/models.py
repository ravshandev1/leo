from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250)
    icon = models.ImageField(upload_to='categories/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, models.CASCADE, 'products')
    name = models.CharField(max_length=250, unique=True)
    bonus = models.PositiveIntegerField(default=1)
    price = models.IntegerField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')

    def __str__(self):
        return self.product.name

    @property
    def image_path(self):
        return self.image.path