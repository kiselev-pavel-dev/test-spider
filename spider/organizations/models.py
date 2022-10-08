from django.core.validators import MinValueValidator
from django.db import models

ERROR_PRICE = "Цена товара должна быть больше или равна нулю!"


class District(models.Model):
    name = models.CharField("Название", max_length=150)

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Район города"
        verbose_name_plural = "Районы городов"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField("Название", max_length=150)

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Категория товара/услуги"
        verbose_name_plural = "Категории товаров/услуг"

    def __str__(self):
        return self.name


class NetworkOrganization(models.Model):
    name = models.CharField("Название", max_length=150)

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Сеть предприятия"
        verbose_name_plural = "Сеть предприятий"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField("Название", max_length=150)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Товар/Услуга"
        verbose_name_plural = "Товары/услуги"

    def __str__(self):
        return f"{self.name} - {self.category}"


class Organization(models.Model):
    name = models.CharField("Название", max_length=150)
    description = models.CharField("Описание", max_length=1000)
    network = models.ForeignKey(
        NetworkOrganization,
        on_delete=models.CASCADE,
        related_name="organizations",
        verbose_name="Сеть предприятия",
    )
    district = models.ManyToManyField(District, through="OrganizationDistrict")
    product = models.ManyToManyField(Product, through="ProductOrganization")

    class Meta:
        ordering = ["-pk"]
        verbose_name = "Предприятие"
        verbose_name_plural = "Предприятия"

    def __str__(self):
        return f"{self.name} - {self.description}"


class OrganizationDistrict(models.Model):
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        related_name="organization_districts",
        verbose_name="Район города",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="organization_districts",
    )

    class Meta:
        verbose_name = "Расположение предприятия"
        verbose_name_plural = "Расположение предприятий"

    def __str__(self):
        return f"{self.district}"


class ProductOrganization(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="product_organizations",
        verbose_name="Товар/Услуга",
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="product_organizations",
        verbose_name="Предприятие",
    )
    price = models.IntegerField(
        "Цена", validators=[MinValueValidator(0, ERROR_PRICE)]
    )

    class Meta:
        verbose_name = "Товары предприятия"
        verbose_name_plural = "Товары предприятий"

    def __str__(self):
        return f"{self.product}"
