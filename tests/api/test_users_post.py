from http import HTTPStatus

import allure
import pytest
from faker import Faker

from tests.api.schemas.user_schema import UserCreate, UserResponse

fake = Faker()


@allure.epic("API Tests")
@allure.feature("Users API")
@allure.story("POST /users")
@pytest.mark.api
class TestCreateUser:
    @allure.title("Создать пользователя с валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_create_user_success(self, users_client, sample_user_data):
        user = UserCreate(**sample_user_data)
        response = users_client.create_user(user)

        assert response.status_code == HTTPStatus.CREATED

        created = UserResponse(**response.json())
        assert created.name == user.name
        assert created.job == user.job
        assert created.id
        assert created.createdAt

    @allure.title("Создать пользователя с русскими данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_user_russian_locale(self, users_client):
        fake_ru = Faker("ru_RU")
        user = UserCreate(name=fake_ru.name(), job=fake_ru.job())

        response = users_client.create_user(user)

        assert response.status_code == HTTPStatus.CREATED
        created = UserResponse(**response.json())
        assert created.name == user.name

    @allure.title("Создать пользователя с спецсимволами")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "name,job",
        [
            pytest.param("John Doe", "QA Engineer", id="english"),
            pytest.param("Иван Иванов", "Тестировщик", id="russian"),
            pytest.param("John123", "Dev_Ops", id="with_numbers"),
            pytest.param("John-Doe", "QA-Engineer", id="with_hyphens"),
            pytest.param(fake.name(), fake.job(), id="faker_generated"),
        ],
    )
    def test_create_user_special_chars(self, users_client, name: str, job: str):
        user = UserCreate(name=name, job=job)
        response = users_client.create_user(user)

        assert response.status_code == HTTPStatus.CREATED
        created = UserResponse(**response.json())
        assert created.name == name
        assert created.job == job

    @allure.title("Создать несколько пользователей последовательно")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_multiple_users(self, users_client, multiple_users_data):
        created_users = []

        for user_data in multiple_users_data:
            user = UserCreate(**user_data)
            response = users_client.create_user(user)

            assert response.status_code == HTTPStatus.CREATED
            created = UserResponse(**response.json())
            created_users.append(created)

        ids = [u.id for u in created_users]
        assert len(ids) == len(set(ids)), "Все ID должны быть уникальными"

    @allure.title("Создать пользователя с пустым именем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_create_user_empty_name(self, users_client):
        response = users_client.create_user_raw({"name": "", "job": "QA"})
        assert response.status_code in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]

    @allure.title("Создать пользователя без тела запроса")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_create_user_no_body(self, users_client):
        response = users_client.post("/users", json_data=None)
        assert response.status_code in [HTTPStatus.BAD_REQUEST, HTTPStatus.UNPROCESSABLE_ENTITY]

    @allure.title("Создать пользователя с невалидным JSON")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_user_invalid_json(self, users_client):
        response = users_client.post(
            "/users", content=b'{"name": "John", "job":}', headers={"Content-Type": "application/json"}
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
