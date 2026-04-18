from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"products", views.ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
    path("seller/profile/", views.seller_profile_create, name="seller-profile-create"),
    path("seller/profile/me/", views.seller_profile_me, name="seller-profile-me"),
]