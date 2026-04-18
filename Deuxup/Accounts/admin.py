from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Product, SellerProfile, User
# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'role', 'is_active')
    search_fields = ('first_name', 'role', 'is_active')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ("Quyền", {'fields': ("role", "is_active", "is_staff", "is_superuser")}),
        ("Thông tin", {'fields': ("groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role"),
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions",)


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("shop_name", "user", "phone", "updated_at")
    search_fields = ("shop_name", "user__email", "phone")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "price", "stock", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "seller__email")