import pytest
from django.contrib.auth.models import User

from organizations.models import District


@pytest.fixture
def district():
    return District.objects.create(name="Тестовый район")


@pytest.fixture
def district_2():
    return District.objects.create(name="Тестовый район 2")


@pytest.fixture
def district_3():
    return District.objects.create(name="Тестовый район 3")


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


class TestDistrictAPI:
    @pytest.mark.django_db(transaction=True)
    def test_district_auth_response(self, user_client):
        url = "/districts/"
        response = user_client.get(url)

        assert (
            response.status_code != 404
        ), f"Страница {url} не найдена, проверьте urls.py"

        assert (
            response.status_code == 200
        ), f"Проверьте, что при GET запросе на {url} возвращается статус 200"

    @pytest.mark.django_db(transaction=True)
    def test_district_no_auth_response(self, client):
        url = "/districts/"
        response = client.get(url)

        assert (
            response.status_code == 401
        ), f"Проверьте, что при GET запросе на {url} неавторизованному пользователю возвращается статус 401"

    @pytest.mark.django_db(transaction=True)
    def test_response_type(self, user_client, district):
        url = "/districts/"
        response = user_client.get(url)
        data = response.json()
        assert (
            type(data) == list
        ), f"Проверьте, что при GET запросе на {url} возвращается список"

    @pytest.mark.django_db(transaction=True)
    def test_response_count_obj(self, user_client, district, district_2):
        url = "/districts/"
        response = user_client.get(url)
        data = response.json()
        assert (
            len(data) == District.objects.count()
        ), f"Проверьте, что при GET запросе на {url} возвращается весь список районов"

    @pytest.mark.django_db(transaction=True)
    def test_response_fields_district(self, user_client, district, district_2):
        url = "/districts/"
        response = user_client.get(url)
        data = response.json()
        test_obj = data[0]
        assert "id" in test_obj, "Проверьте, что возвращается id районов"
        assert "name" in test_obj, "Проверьте, что возвращается name районов"

    @pytest.mark.django_db(transaction=True)
    def test_auth_district_create(self, user_client, district, district_2):
        url = "/districts/"
        count_district = District.objects.count()
        data = {}
        response = user_client.post(url, data=data)
        assert (
            response.status_code == 400
        ), f"Проверьте, что при POST запросе на {url} с неверными данными возвращается код 400"
        data = {"name": "Тест"}
        response = user_client.post(url, data=data)
        assert (
            response.status_code == 201
        ), f"Проверьте, что с корректными данными при POST запросе на {url} возвращается статус 201"

        test_data = response.json()
        assert (
            type(test_data) == dict
        ), "Проверьте, что при создании района возвращается словарь с корректными данными"
        assert (
            test_data.get("name") == data["name"]
        ), "Проверьте, что при создании района возвращается словарь с корректными данными"
        assert (
            count_district + 1 == District.objects.count()
        ), f"Проверьте, что при POST запросе на {url} добавился обьект"

    @pytest.mark.django_db(transaction=True)
    def test_no_auth_district_create(self, client, district, district_2):
        url = "/districts/"
        count_district = District.objects.count()
        data = {"name": "Тест"}
        response = client.post(url, data=data)
        assert (
            response.status_code == 401
        ), f"Проверьте, что неавторизованный пользователь при POST запросе на {url} получает код 401"
        assert (
            count_district == District.objects.count()
        ), f"Проверьте, что при POST запросе неавторизованного пользователя на {url} не добавился обьект"

    @pytest.mark.django_db(transaction=True)
    def test_get_current_district(self, user_client, district):
        url = f"/districts/{district.pk}/"
        response = user_client.get(url)

        assert (
            response.status_code == 200
        ), f"Страница {url} не найдена, проверьте urls.py"

        test_data = response.json()
        assert (
            test_data.get("name") == district.name
        ), f"Проверьте, что при GET запросе на {url} возвращаются корректные данные"

    @pytest.mark.django_db(transaction=True)
    def test_patch_current_district(self, user_client, district):
        url = f"/districts/{district.pk}/"
        data = {"name": "Новое название"}
        response = user_client.patch(url, data=data)

        assert (
            response.status_code == 200
        ), f"Проверьте, что при PATCH запросе для авторизованного пользователя возвращается код 200"

        test_district = District.objects.filter(pk=district.pk).first()

        assert (
            test_district
        ), f"Проверьте, что при PATCH запросе на {url} вы не удалили район"

        assert (
            test_district.name == "Новое название"
        ), f"Проверьте, что при PATCH запросе на {url} вы поменяли название района"

    @pytest.mark.django_db(transaction=True)
    def test_auth_delete_current_district(self, user_client, district):
        url = f"/districts/{district.pk}/"
        response = user_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Проверьте, что при DELETE запросе на {url} возвращается статус 204"

        test_district = District.objects.filter(pk=district.pk).first()

        assert (
            not test_district
        ), f"Проверьте, что при DELETE запросе на {url} вы удалили обьект"

    @pytest.mark.django_db(transaction=True)
    def test_unauth_delete_current_district(self, client, district):
        count_district = District.objects.count()
        url = url = f"/districts/{district.pk}/"
        response = client.delete(url)

        assert (
            response.status_code == 401
        ), f"Проверьте, что неавторизованному пользователю при DELETE запросе на {url} возвращается статус 401"

        assert (
            count_district == District.objects.count()
        ), f"Проверьте, что неавторизованный пользователь при DELETE запросе на {url} не удаляет район"
