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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Faqat birinchi bonusni qaytarish uchun:
        first_bonus = qs.first()
        if first_bonus:
            # QuerySetga o'rash uchun: [first_bonus] orqali bir elementli ro'yxat qaytariladi
            return qs.filter(id=first_bonus.id)
        return qs.none()


@admin.register(Product)
class ProductAdmin(CustomAdmin):
    inlines = [ProductImageInline, ProductBonusInline]
    list_display = ['id', 'name', 'price', 'category']
