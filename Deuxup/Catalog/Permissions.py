from rest_framework.permissions import BasePermission, SAFE_METHODS

from accounts.permissions import IsSeller, IsOwnerOrReadOnly

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, "role", None) == "seller")

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        u = request.user
        return bool(u and u.is_authenticated and getattr(u, "role", None) == "admin")

class IsSellerOrReadOnly(BasePermission):

    message = "Chỉ tài khoản Seller mới có quyền."
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
            return IsSeller().has_permission(request,view)

class IsOwnerOrAdmin(BasePermission):
    message = "Chỉ tài khoản chủ sở hữu hoặc Admin mới có quyền."

    def has_object_permission(self, request, view, obj):
        u = request.user
        if not u or not u.is_authenticated:
            return False
        if getattr(u, "role", None) == u.Role.ADMIN:
            return True
        profile = getattr(u, "seller_profile", None)
        if profile is None:
            return False
        return bool(profile.id == obj.seller.pk)
