from email.mime import base
from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (
    OrganizationAll,
    OrganizationViewSet,
    ProductViewSet,
    CategoryViewSet,
    DistrictViewSet,
    NetworkOrganizationViewSet,
)

app_name = "api"

router = DefaultRouter()

router.register("products", ProductViewSet, basename="products")
router.register("categories", CategoryViewSet, basename="categories")
router.register("districts", DistrictViewSet, basename="districts")
router.register("networks", NetworkOrganizationViewSet, basename="networks")
router.register(
    "organizations/(?P<district_id>\d+)",
    OrganizationViewSet,
    basename="organizations",
)
router.register(
    "organizations_all",
    OrganizationAll,
    basename="organizations_detail",
)

urlpatterns = [
    path("", include(router.urls)),
    path('auth/', views.obtain_auth_token),
]
