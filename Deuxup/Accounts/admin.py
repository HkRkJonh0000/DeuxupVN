from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    list_display = ("email", "first_name", "last_name", "is_staff", "role", "is_active")
    search_fields = ("first_name", "email", "role")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Quyền", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Thông tin", {"fields": ("groups", "user_permissions")}),
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
    filter_horizontal = ("groups", "user_permissions")