from django.shortcuts import get_object_or_404
from rest_framework import serializers

from organizations.models import (
    Category,
    District,
    NetworkOrganization,
    Organization,
    OrganizationDistrict,
    Product,
    ProductOrganization,
)

ERROR_PRICE = "Цена товара должна быть больше или равна нулю!"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ("id", "name")


class NetworkOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkOrganization
        fields = ("id", "name")


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ("id", "name", "category")

    def create(self, validated_data):
        category_id = validated_data.pop("category")["name"]
        category = get_object_or_404(Category, pk=category_id)
        product = Product.objects.create(category=category, **validated_data)
        return product


class ProductInOrganizationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product.pk',
    )
    name = serializers.CharField(read_only=True, source='product.name')
    category = serializers.CharField(source="product.category.name")

    class Meta:
        model = ProductOrganization
        fields = ('id', 'name', 'category', 'price')


class OrganizationSerializer(serializers.ModelSerializer):
    product = ProductInOrganizationSerializer(
        many=True, source='product_organizations'
    )
    district = DistrictSerializer(many=True)
    network = serializers.CharField(source='network.name')
    count_products = serializers.SerializerMethodField()
    count_districts = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "description",
            "network",
            "count_products",
            "count_districts",
            "district",
            "product",
        )

    def get_count_products(self, obj):
        return ProductOrganization.objects.filter(organization=obj).count()

    def get_count_districts(self, obj):
        return OrganizationDistrict.objects.filter(organization=obj).count()


class ProductWriteOrganizationSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.IntegerField()

    class Meta:
        model = ProductOrganization
        fields = ("id", "price")

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError(ERROR_PRICE)
        return value


class OrganizationWriteSerializer(serializers.ModelSerializer):
    district = serializers.PrimaryKeyRelatedField(
        queryset=District.objects.all(), many=True
    )
    product = ProductWriteOrganizationSerializer(many=True)

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "description",
            "network",
            "district",
            "product",
        )

    def create(self, validated_data):
        districts = validated_data.pop("district")
        products = validated_data.pop("product")
        organization = Organization.objects.create(**validated_data)
        products = self.context["request"].data["product"]
        districts_list = [
            OrganizationDistrict(district=district, organization=organization)
            for district in districts
        ]
        OrganizationDistrict.objects.bulk_create(districts_list)
        produsts_list = []
        for product in products:
            product_obj = get_object_or_404(Product, pk=product["id"])
            produsts_list.append(
                ProductOrganization(
                    product=product_obj,
                    organization=organization,
                    price=product["price"],
                )
            )
        ProductOrganization.objects.bulk_create(produsts_list)
        return organization

    def update(self, instance, validated_data):
        districts = validated_data.pop("district")
        products = validated_data.pop("product")
        products = self.context["request"].data["product"]
        ProductOrganization.objects.filter(organization=instance).delete()
        produsts_list = []
        for product in products:
            product_obj = get_object_or_404(Product, pk=product["id"])
            produsts_list.append(
                ProductOrganization(
                    product=product_obj,
                    organization=instance,
                    price=product["price"],
                )
            )
        ProductOrganization.objects.bulk_create(produsts_list)
        instance.district.set(districts)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description
        )
        instance.network = validated_data.get('network', instance.network)
        instance.save()
        return instance

    def to_representation(self, instance):
        return OrganizationSerializer(instance, context=self.context).data
