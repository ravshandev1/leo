from django.contrib import admin
from .models import Category, Product, ProductImage, Order, SubCategory
from .translations import CustomAdmin, StackedAdmin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'count', 'store', 'created_at']


class SubCategoryInline(StackedAdmin):
    model = SubCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(CustomAdmin):
    list_display = ['id', 'name', 'created_at']
    inlines = [SubCategoryInline]


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(CustomAdmin):
    inlines = [ProductImageInline]
    list_display = ['id', 'name', 'price', 'category', 'bonus', 'created_at']
