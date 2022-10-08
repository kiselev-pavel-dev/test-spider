import pytest
from django.contrib.auth.models import User

from organizations.models import Category


@pytest.fixture
def category():
    return Category.objects.create(name="Тестовая категория")


@pytest.fixture
def category_2():
    return Category.objects.create(name="Тестовая категория 2")


@pytest.fixture
def category_3():
    return Category.objects.create(name="Тестовая категория 3")


@pytest.fixture
def user():
    return User.objects.create_user(username="TestUser", password="1234567")


@pytest.fixture
def client():
    from rest_framework.test import APIClient

    client = APIClient()
    return client


@pytest.fixture
def token(user):
    from rest_framework.authtoken.models import Token

    token, _ = Token.objects.get_or_create(user=user)
    return token.key


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return client


class TestCategoryAPI:
    url = "/categories/"

    @pytest.mark.django_db(transaction=True)
    def test_category_auth_response(self, user_client):
        response = user_client.get(self.url)

        assert (
            response.status_code != 404
        ), f"Страница {self.url} не найдена, проверьте urls.py"

        assert (
            response.status_code == 200
        ), f"Проверьте, что при GET запросе на {self.url} возвращается статус 200"

    @pytest.mark.django_db(transaction=True)
    def test_category_no_auth_response(self, client):
        response = client.get(self.url)

        assert (
            response.status_code == 401
        ), f"Проверьте, что при GET запросе на {self.url} неавторизованному пользователю возвращается статус 401"

    @pytest.mark.django_db(transaction=True)
    def test_response_type(self, user_client, category):
        response = user_client.get(self.url)
        data = response.json()
        assert (
            type(data) == list
        ), f"Проверьте, что при GET запросе на {self.url} возвращается список"

    @pytest.mark.django_db(transaction=True)
    def test_response_count_obj(self, user_client, category, category_2):
        response = user_client.get(self.url)
        data = response.json()
        assert (
            len(data) == Category.objects.count()
        ), f"Проверьте, что при GET запросе на {self.url} возвращается весь список категорий"

    @pytest.mark.django_db(transaction=True)
    def test_response_fields_category(self, user_client, category, category_2):
        response = user_client.get(self.url)
        data = response.json()
        test_obj = data[0]
        assert "id" in test_obj, "Проверьте, что возвращается id категорий"
        assert "name" in test_obj, "Проверьте, что возвращается name категорий"

    @pytest.mark.django_db(transaction=True)
    def test_auth_category_create(self, user_client, category, category_2):
        count_category = Category.objects.count()
        data = {}
        response = user_client.post(self.url, data=data)
        assert (
            response.status_code == 400
        ), f"Проверьте, что при POST запросе на {self.url} с неверными данными возвращается код 400"
        data = {"name": "Тест"}
        response = user_client.post(self.url, data=data)
        assert (
            response.status_code == 201
        ), f"Проверьте, что с корректными данными при POST запросе на {self.url} возвращается статус 201"

        test_data = response.json()
        assert (
            type(test_data) == dict
        ), "Проверьте, что при создании категории возвращается словарь с корректными данными"
        assert (
            test_data.get("name") == data["name"]
        ), "Проверьте, что при создании категории возвращается словарь с корректными данными"
        assert (
            count_category + 1 == Category.objects.count()
        ), f"Проверьте, что при POST запросе на {self.url} добавился объект"

    @pytest.mark.django_db(transaction=True)
    def test_no_auth_category_create(self, client, category, category_2):
        count_category = Category.objects.count()
        data = {"name": "Тест"}
        response = client.post(self.url, data=data)
        assert (
            response.status_code == 401
        ), f"Проверьте, что неавторизованный пользователь при POST запросе на {self.url} получает код 401"
        assert (
            count_category == Category.objects.count()
        ), f"Проверьте, что при POST запросе неавторизованного пользователя на {self.url} не добавился объект"

    @pytest.mark.django_db(transaction=True)
    def test_get_current_category(self, user_client, category):
        url = f"/categories/{category.pk}/"
        response = user_client.get(url)

        assert (
            response.status_code == 200
        ), f"Страница {url} не найдена, проверьте urls.py"

        test_data = response.json()
        assert (
            test_data.get("name") == category.name
        ), f"Проверьте, что при GET запросе на {url} возвращаются корректные данные"

    @pytest.mark.django_db(transaction=True)
    def test_patch_current_category(self, user_client, category):
        url = f"/categories/{category.pk}/"
        data = {"name": "Новое название"}
        response = user_client.patch(url, data=data)

        assert (
            response.status_code == 200
        ), f"Проверьте, что при PATCH запросе для авторизованного пользователя возвращается код 200"

        test_category = Category.objects.filter(pk=category.pk).first()

        assert (
            test_category
        ), f"Проверьте, что при PATCH запросе на {url} вы не удалили объект"

        assert (
            test_category.name == "Новое название"
        ), f"Проверьте, что при PATCH запросе на {url} вы поменяли название объекта"

    @pytest.mark.django_db(transaction=True)
    def test_auth_delete_current_category(self, user_client, category):
        url = f"/categories/{category.pk}/"
        response = user_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Проверьте, что при DELETE запросе на {url} возвращается статус 204"

        test_category = Category.objects.filter(pk=category.pk).first()

        assert (
            not test_category
        ), f"Проверьте, что при DELETE запросе на {url} вы удалили объект"

    @pytest.mark.django_db(transaction=True)
    def test_unauth_delete_current_category(self, client, category):
        count_category = Category.objects.count()
        url = url = f"/categories/{category.pk}/"
        response = client.delete(url)

        assert (
            response.status_code == 401
        ), f"Проверьте, что неавторизованному пользователю при DELETE запросе на {url} возвращается статус 401"

        assert (
            count_category == Category.objects.count()
        ), f"Проверьте, что неавторизованный пользователь при DELETE запросе на {url} не удаляет обЪект"
