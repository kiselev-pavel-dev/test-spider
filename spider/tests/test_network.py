import pytest
from django.contrib.auth.models import User

from organizations.models import NetworkOrganization


@pytest.fixture
def network():
    return NetworkOrganization.objects.create(name="Тестовая сеть предприятий")


@pytest.fixture
def network_2():
    return NetworkOrganization.objects.create(
        name="Тестовая сеть предприятий 2"
    )


@pytest.fixture
def network_3():
    return NetworkOrganization.objects.create(
        name="Тестовая сеть предприятий 3"
    )


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
    url = "/networks/"

    @pytest.mark.django_db(transaction=True)
    def test_network_auth_response(self, user_client):
        response = user_client.get(self.url)

        assert (
            response.status_code != 404
        ), f"Страница {self.url} не найдена, проверьте urls.py"

        assert (
            response.status_code == 200
        ), f"Проверьте, что при GET запросе на {self.url} возвращается статус 200"

    @pytest.mark.django_db(transaction=True)
    def test_network_no_auth_response(self, client):
        response = client.get(self.url)

        assert (
            response.status_code == 401
        ), f"Проверьте, что при GET запросе на {self.url} неавторизованному пользователю возвращается статус 401"

    @pytest.mark.django_db(transaction=True)
    def test_response_type(self, user_client, network):
        response = user_client.get(self.url)
        data = response.json()
        assert (
            type(data) == list
        ), f"Проверьте, что при GET запросе на {self.url} возвращается список"

    @pytest.mark.django_db(transaction=True)
    def test_response_count_obj(self, user_client, network, network_2):
        response = user_client.get(self.url)
        data = response.json()
        assert (
            len(data) == NetworkOrganization.objects.count()
        ), f"Проверьте, что при GET запросе на {self.url} возвращаются все объекты"

    @pytest.mark.django_db(transaction=True)
    def test_response_fields_network(self, user_client, network, network_2):
        response = user_client.get(self.url)
        data = response.json()
        test_obj = data[0]
        assert "id" in test_obj, "Проверьте, что возвращается id сети"
        assert "name" in test_obj, "Проверьте, что возвращается name сети"

    @pytest.mark.django_db(transaction=True)
    def test_auth_network_create(self, user_client, network, network_2):
        count_network = NetworkOrganization.objects.count()
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
        ), "Проверьте, что при создании сети возвращается словарь с корректными данными"
        assert (
            test_data.get("name") == data["name"]
        ), "Проверьте, что при создании сети возвращается словарь с корректными данными"
        assert (
            count_network + 1 == NetworkOrganization.objects.count()
        ), f"Проверьте, что при POST запросе на {self.url} добавился объект"

    @pytest.mark.django_db(transaction=True)
    def test_no_auth_network_create(self, client, network, network_2):
        count_network = NetworkOrganization.objects.count()
        data = {"name": "Тест"}
        response = client.post(self.url, data=data)
        assert (
            response.status_code == 401
        ), f"Проверьте, что неавторизованный пользователь при POST запросе на {self.url} получает код 401"
        assert (
            count_network == NetworkOrganization.objects.count()
        ), f"Проверьте, что при POST запросе неавторизованного пользователя на {self.url} не добавился объект"

    @pytest.mark.django_db(transaction=True)
    def test_get_current_network(self, user_client, network):
        url = f"/networks/{network.pk}/"
        response = user_client.get(url)

        assert (
            response.status_code == 200
        ), f"Страница {url} не найдена, проверьте urls.py"

        test_data = response.json()
        assert (
            test_data.get("name") == network.name
        ), f"Проверьте, что при GET запросе на {url} возвращаются корректные данные"

    @pytest.mark.django_db(transaction=True)
    def test_patch_current_network(self, user_client, network):
        url = f"/networks/{network.pk}/"
        data = {"name": "Новое название"}
        response = user_client.patch(url, data=data)

        assert (
            response.status_code == 200
        ), f"Проверьте, что при PATCH запросе для авторизованного пользователя возвращается код 200"

        test_network = NetworkOrganization.objects.filter(
            pk=network.pk
        ).first()

        assert (
            test_network
        ), f"Проверьте, что при PATCH запросе на {url} вы не удалили обЪект"

        assert (
            test_network.name == "Новое название"
        ), f"Проверьте, что при PATCH запросе на {url} вы поменяли название обЪекта"

    @pytest.mark.django_db(transaction=True)
    def test_auth_delete_current_network(self, user_client, network):
        url = f"/networks/{network.pk}/"
        response = user_client.delete(url)

        assert (
            response.status_code == 204
        ), f"Проверьте, что при DELETE запросе на {url} возвращается статус 204"

        test_network = NetworkOrganization.objects.filter(
            pk=network.pk
        ).first()

        assert (
            not test_network
        ), f"Проверьте, что при DELETE запросе на {url} вы удалили объект"

    @pytest.mark.django_db(transaction=True)
    def test_unauth_delete_current_network(self, client, network):
        count_network = NetworkOrganization.objects.count()
        url = url = f"/networks/{network.pk}/"
        response = client.delete(url)

        assert (
            response.status_code == 401
        ), f"Проверьте, что неавторизованному пользователю при DELETE запросе на {url} возвращается статус 401"

        assert (
            count_network == NetworkOrganization.objects.count()
        ), f"Проверьте, что неавторизованный пользователь при DELETE запросе на {url} не удаляет объект"
