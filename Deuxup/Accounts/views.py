from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Products.models import Product, SellerProfile
from .permissions import IsOwnerOrReadOnly, IsSeller
from .serializers import (
    LoginSerializer,
    ProductSerializer,
    RegisterSerializer,
    SellerProfileSerializer,
    UserSerializer,
)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": UserSerializer(user).data}, status=status.HTTP_200_OK)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class SellerProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSeller]

    def get(self, request):
        profile, _ = SellerProfile.objects.get_or_create(
            user=request.user, defaults={"shop_name": request.user.email.split("@")[0]}
        )
        return Response(SellerProfileSerializer(profile).data, status=status.HTTP_200_OK)

    def put(self, request):
        profile, _ = SellerProfile.objects.get_or_create(
            user=request.user, defaults={"shop_name": request.user.email.split("@")[0]}
        )
        serializer = SellerProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("seller").all()

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return [IsAuthenticated(), IsSeller(), IsOwnerOrReadOnly()]
        return [AllowAny()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action in ("update", "partial_update", "destroy"):
            user = getattr(self.request, "user", None)
            if user and user.is_authenticated:
                return qs.filter(seller=user)
            return qs.none()
        if self.request and self.request.user and self.request.user.is_authenticated and self.request.user.role == "seller":
            if self.request.query_params.get("mine") == "1":
                return qs.filter(seller=self.request.user)
        return qs.filter(is_active=True)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class _SellerProductBaseAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSeller, IsOwnerOrReadOnly]

    def _get_product(self, pk: int) -> Product:
        product = Product.objects.select_related("seller").get(pk=pk)
        self.check_object_permissions(self.request, product)
        return product


class SellerProductsAPIView(_SellerProductBaseAPIView):
    def get(self, request):
        qs = Product.objects.select_related("seller").filter(seller=request.user)
        return Response(ProductSerializer(qs, many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SellerProductDetailAPIView(_SellerProductBaseAPIView):
    def get(self, request, pk: int):
        product = self._get_product(pk)
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class SellerProductActivateAPIView(_SellerProductBaseAPIView):
    def post(self, request, pk: int):
        product = self._get_product(pk)
        product.is_active = True
        product.save(update_fields=["is_active"])
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class SellerProductDeactivateAPIView(_SellerProductBaseAPIView):
    def post(self, request, pk: int):
        product = self._get_product(pk)
        product.is_active = False
        product.save(update_fields=["is_active"])
        return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)


class SellerProductDeleteAPIView(_SellerProductBaseAPIView):
    def delete(self, request, pk: int):
        product = self._get_product(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SellerProductEditAPIView(_SellerProductBaseAPIView):
    def put(self, request, pk: int):
        product = self._get_product(pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk: int):
        product = self._get_product(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(seller=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SellerProductCreateAPIView(SellerProductEditAPIView):
    pass