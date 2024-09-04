from django.contrib import admin
from .models import Region, TelegramUser, UserPoint, VerifyPhone, Bonus, InfoPhone, Info, StorePhone, \
    Store
from .translations import CustomAdmin


class StorePhoneInline(admin.StackedInline):
    model = StorePhone
    extra = 0


class InfoPhoneInline(admin.StackedInline):
    model = InfoPhone
    extra = 0


@admin.register(Store)
class StoreAdmin(CustomAdmin):
    inlines = [StorePhoneInline]
    list_display = ['id', 'name']


@admin.register(Info)
class InfoAdmin(admin.ModelAdmin):
    inlines = [InfoPhoneInline]


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


@admin.register(UserPoint)
class UserPointAdmin(admin.ModelAdmin):
    list_display = ["user", "bonus", "is_active", "created_at"]
