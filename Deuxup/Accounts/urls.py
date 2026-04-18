from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    LoginAPIView,
    MeAPIView,
    ProductViewSet,
    RegisterAPIView,
    SellerProfileAPIView,
    SellerProductActivateAPIView,
    SellerProductCreateAPIView,
    SellerProductDeactivateAPIView,
    SellerProductDeleteAPIView,
    SellerProductDetailAPIView,
    SellerProductEditAPIView,
    SellerProductsAPIView,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("auth/register/", RegisterAPIView.as_view(), name="auth-register"),
    path("auth/login/", LoginAPIView.as_view(), name="auth-login"),
    path("auth/me/", MeAPIView.as_view(), name="auth-me"),
    path("seller/profile/", SellerProfileAPIView.as_view(), name="seller-profile"),
    path("seller/products/", SellerProductsAPIView.as_view(), name="seller-products"),
    path("seller/products/<int:pk>/", SellerProductDetailAPIView.as_view(), name="seller-product-detail"),
    path("seller/products/<int:pk>/activate/", SellerProductActivateAPIView.as_view(), name="seller-product-activate"),
    path("seller/products/<int:pk>/deactivate/", SellerProductDeactivateAPIView.as_view(), name="seller-product-deactivate"),
    path("seller/products/<int:pk>/delete/", SellerProductDeleteAPIView.as_view(), name="seller-product-delete"),
    path("seller/products/<int:pk>/edit/", SellerProductEditAPIView.as_view(), name="seller-product-edit"),
    path("seller/products/<int:pk>/update/", SellerProductCreateAPIView.as_view(), name="seller-product-update"),
    path("", include(router.urls)),
]
