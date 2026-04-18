from django.shortcuts import render
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from Accounts.models import User

from .models import Product, SellerProfile
from .Permissions import IsAdmin, IsOwnerSellerOrAdmin, IsSeller, IsSellerOrReadOnly
from .serializers import ProductSerializer, SellerProfileSerializer

@api_view(["GET", "PATCH"])
@permission_classes([permissions.IsAuthenticated, IsSeller])
def seller_profile_me(request):
    try:
        profile = request.user.seller_profile
    except SellerProfile.DoesNotExist:
        if request.method == "GET":
            return Response({"detail": "Chưa có shop."}, status=404)
        return Response({"detail": "Dùng POST /api/seller/profile/ để tạo shop."}, status=400)

    if request.method == "GET":
        return Response(SellerProfileSerializer(profile).data)
    ser = SellerProfileSerializer(profile, data=request.data, partial=True, context={"request": request})
    ser.is_valid(raise_exception=True)
    ser.save()
    return Response(ser.data)


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated, IsSeller])
def seller_profile_create(request):
    if SellerProfile.objects.filter(user=request.user).exists():
        return Response({"detail": "Đã có shop."}, status=400)
    ser = SellerProfileSerializer(data=request.data, context={"request": request})
    ser.is_valid(raise_exception=True)
    ser.save()
    return Response(ser.data, status=201)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related("seller", "seller__user").all()
    serializer_class = ProductSerializer
    permission_classes = [IsSellerOrReadOnly, IsOwnerSellerOrAdmin]
    lookup_field = "pk"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ("list", "retrieve"):
            qs = qs.filter(is_active=True)
        return qs

    def get_permissions(self):
        if self.action in ("update", "partial_update", "destroy"):
            return [permissions.IsAuthenticated(), IsOwnerSellerOrAdmin()]
        return super().get_permissions()
