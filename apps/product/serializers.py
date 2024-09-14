from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage, Cart, Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['product', 'count', 'store', 'total']


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'sub_categories']

    sub_categories = SubCategorySerializer(many=True, read_only=True)
    icon = serializers.CharField(source='icon_url')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    image = serializers.CharField(source='image_url')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'bonus', 'price', 'description']

    bonus = serializers.CharField(source='bonus.point')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['name', 'price', 'count']

    name = serializers.CharField(source='product.name')
    price = serializers.CharField(source='price.name')
