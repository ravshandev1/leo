from django.contrib import admin
from .models import Category, Product, ProductImage, Order, SubCategory, Bonus, UserSumma
from .translations import CustomAdmin, StackedAdmin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'created_at']
    list_filter = ['created_at', 'store']


@admin.register(UserSumma)
class UserSummaAdmin(admin.ModelAdmin):
    list_display = ['user', 'bonus', 'created_at']
    list_filter = ['created_at', 'user']


class SubCategoryInline(StackedAdmin):
    model = SubCategory
    extra = 0


@admin.register(Category)
class CategoryAdmin(CustomAdmin):
    list_display = ['id', 'name']
    inlines = [SubCategoryInline]


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0


class ProductBonusInline(admin.StackedInline):
    model = Bonus
    extra = 0


@admin.register(Product)
class ProductAdmin(CustomAdmin):
    inlines = [ProductImageInline, ProductBonusInline]
    list_display = ['id', 'name', 'price', 'category']
