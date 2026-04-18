from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSeller(BasePermission):
    message = "Chỉ tài khoản Seller mới có quyền."

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(user, "role", None) == "seller")


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = getattr(request, "user", None)
        return bool(user and user.is_authenticated and getattr(obj, "seller_id", None) == user.id)

