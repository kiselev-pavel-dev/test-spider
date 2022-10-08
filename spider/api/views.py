from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from organizations.models import (
    Organization,
    Product,
    Category,
    District,
    NetworkOrganization,
)
from .filters import OrganizationFilter

from .serializers import (
    OrganizationSerializer,
    ProductSerializer,
    CategorySerializer,
    DistrictSerializer,
    NetworkOrganizationSerializer,
    OrganizationWriteSerializer,
)


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DistrictViewSet(ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer


class NetworkOrganizationViewSet(ModelViewSet):
    queryset = NetworkOrganization.objects.all()
    serializer_class = NetworkOrganizationSerializer


class OrganizationViewSet(ReadOnlyModelViewSet):
    serializer_class = OrganizationSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = OrganizationFilter
    search_fields = ("^product__name",)

    def get_queryset(self, **kwargs):
        district_id = self.kwargs.get("district_id")
        return Organization.objects.filter(district=district_id)


class OrganizationAll(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OrganizationSerializer
        return OrganizationWriteSerializer
