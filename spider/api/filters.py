from django_filters import rest_framework as filters

from organizations.models import Organization, Category


class OrganizationFilter(filters.FilterSet):
    categories = filters.ModelMultipleChoiceFilter(
        field_name="product__category__name",
        to_field_name="name",
        queryset=Category.objects.all(),
    )

    class Meta:
        model = Organization
        fields = ("categories",)
