from django.contrib import admin

from .models import (Category, District, NetworkOrganization, Organization,
                     OrganizationDistrict, Product, ProductOrganization)


class DistrictAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


class NetworkOrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]


class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "category"]
    search_fields = ["name"]
    list_display_links = ["id", "name"]


class DistrictsInline(admin.TabularInline):
    model = OrganizationDistrict
    extra = 1


class ProductOrganizationInline(admin.TabularInline):
    model = ProductOrganization
    extra = 1


class ProductOrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "organization", "product", "price"]
    list_display_links = ["id", "organization"]


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "description", "network"]
    list_display_links = ["id", "name"]
    search_fields = ["name"]
    inlines = (DistrictsInline, ProductOrganizationInline)


admin.site.register(District, DistrictAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(NetworkOrganization, NetworkOrganizationAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProductOrganization, ProductOrganizationAdmin)
