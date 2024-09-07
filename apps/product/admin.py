from django.contrib import admin
from .models import Category, Product, ProductImage, Order
from .translations import CustomAdmin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'count', 'store', 'created_at']


@admin.register(Category)
class CategoryAdmin(CustomAdmin):
    list_display = ['id', 'name', 'created_at']


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(CustomAdmin):
    inlines = [ProductImageInline]
    list_display = ['id', 'name', 'price', 'category', 'bonus', 'created_at']
