from django.contrib import admin
from .models import Category, Product, ProductImage, Order, SubCategory, ProductAdminForm
from .translations import CustomAdmin, StackedAdmin


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'created_at']
    list_filter = ['created_at', 'store']


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


@admin.register(Product)
class ProductAdmin(CustomAdmin):
    inlines = [ProductImageInline]
    list_display = ['id', 'name', 'price', 'category', 'bonus']
    form = ProductAdminForm

    def save_model(self, request, obj, form, change):
        if not change:  # Agar mahsulot yangilanayotgan bo'lsa
            obj.bonus.has_product = True  # Bonusni mahsulot bilan bog'liq qilib belgilang
            obj.bonus.save()
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Agar mahsulot yangilanayotgan bo'lsa, bonusni readonly qilamiz
            return ['bonus']
        return []
