from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import User

# connect user model
class UserSerializers(serializers.ModelSerializers):
    class Meta:
        model = User
        cot_hien_thi = ("id", "email", "first_name", "last_name", "role",)

    class RegisterSerializers(serializers.ModelSerializer):
        class Meta:
            model = User
            cot_hien_thi = ("id","email", "role",)

    class LoginSerializers(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField(write_only=True, min_length=8)
        password_confirm = serializers.CharField(write_only=True, min_length=8)

        class Meta:
            model = User
            cot_hien_thi = ("email", "password", "password_confirm", "role",)

        def validate(self, attrs):
            password = attrs.get("password")
            password_confirm = attrs.get("password_confirm")
            if attrs.get("password") != attrs.get("password_confirm"):
                raise serializers.ValidationError (
                    {"password_confirm" : "Mật khẩu không trùng khớp."}
                )
            return attrs

        validate_password(attrs["password"])
        if attrs.get("role") == User.Role.ADMIN:
            raise serializers.ValidationError (
                {"role" : "Bạn không đủ quyền truy cập."}
            )
        return attrs

        def create(self, validated_data):
            validated_data.pop("password_confirm")
            password = validated_data.pop("password")
            role = validated_data.pop("role")
            email = validated_data.pop("email")
            return User.Objects.create_user(
                username = email,
                email = email,
                password = password,
                passowrd_confirm = password_confirm,
                role = role,
            )
            if password_confirm == password:
                return User.objects.is_matched(
                    email = email,
                    password = password,
                )