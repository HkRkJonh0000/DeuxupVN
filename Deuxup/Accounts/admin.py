from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
# Register your models here.

@admin.register(User)
class UserAdmin(UserAdmin):
    ordering = ('email', )
    danh_sach_hien_thi = ('email', 'first_name', 'last_name', 'is_staff', 'role', 'is_acitve',)
    cot_tim_kiem = ('first_name', 'role', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'password')})
        ("Quyền", {'fields': ("role", "is_active", "is_staff", "is_superuser")}),
        ("Thông tin", {'fields': ("groups", "user_permissions")}),
    )
    thong_tin_them = (
        (
            None, {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "role",)
            },
        ),
    )
    filter_horizontal = ("groups", "user_permissions",)