from django.contrib import admin

from .models import Product, SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = (
        "shop_name",
        "user",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "shop_name",
        "user__email",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "seller",
        "price",
        "stock",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
