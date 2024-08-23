from django.contrib import admin
from .models import Region, TelegramUser, UserPoint, UserPointImage, VerifyPhone, Bonus
from .translations import CustomAdmin


@admin.register(Region)
class RegionAdmin(CustomAdmin):
    list_display = ["id", "name"]


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ["phone", "name", "region", "point", "lang", "created_at"]


@admin.register(VerifyPhone)
class VerifyPhoneAdmin(admin.ModelAdmin):
    list_display = ["phone", "code", "created_at"]


@admin.register(Bonus)
class BonusAdmin(admin.ModelAdmin):
    list_display = ["code", "point", "created_at"]


class UserPointImageInline(admin.StackedInline):
    model = UserPointImage
    extra = 0


@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    inlines = [UserPointImageInline]
    list_display = ["user", "bonus", "is_active", "created_at"]