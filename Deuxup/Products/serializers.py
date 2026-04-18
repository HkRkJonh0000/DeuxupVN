from rest_framework import serializers

from Accounts.models import User
from Accounts.serializers import UserSerializer
from .models import Product, SellerProfile


class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = SellerProfile
        fields = ("user", "shop_name", "description", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        if getattr(user, "role", None) != user.Role.SELLER:
            raise serializers.ValidationError("Bạn không có quyền tạo SellerProfile.")
        if SellerProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError("Tên cửa hàng đã tồn tại.")
        return SellerProfile.objects.create(user=user, **validated_data)

class ProductSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(source="seller.shop_name", read_only=True)
    
    class Meta:
        model = Product
        fields = (
            "id",
            "shop_name",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "shop_name",
            "slug",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        try:
            profile = user.seller_profile
        except SellerProfile.DoesNotExist:
            raise serializers.ValidationError("Tạo Profile trước khi tạo sản phẩm.")
        return Product.objects.create(seller=profile, **validated_data)