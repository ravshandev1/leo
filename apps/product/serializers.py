from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage, Cart, Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'count']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['products', 'store', 'total']

    products = OrderProductSerializer(many=True)


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
        fields = ['id', 'name', 'bonus', 'price', 'description', 'images']

    bonus = serializers.CharField(source='bonus.summa')
    images = ProductImageSerializer(many=True, read_only=True)


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['name', 'image', 'price', 'count']

    name = serializers.CharField(source='product.name')
    price = serializers.CharField(source='price.name')
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.product.images.first().url
