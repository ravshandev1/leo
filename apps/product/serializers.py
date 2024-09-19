from rest_framework import serializers
from .models import Category, SubCategory, Product, ProductImage, Cart, Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'count']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['user', 'products', 'store', 'total']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        user = validated_data.get('user')
        order = Order.objects.create(user_id=user.id, **validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, **product_data)
        return order

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
        fields = ['id', 'name', 'image', 'price', 'count']

    id = serializers.CharField(source='product.id')
    name = serializers.CharField(source='product.name')
    price = serializers.CharField(source='product.price')
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        return obj.product.images.first().image_url
