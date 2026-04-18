from rest_framework import serializers

from accounts.models import User
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
        if SellerProfile.Objects.filter(user=user).exits:
            raise serializers.ValidationError("Tên cửa hàng đã tồn tại.")
        return SellerProfile.objects.create(user=user, **validated_data)