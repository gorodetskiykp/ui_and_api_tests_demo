from http import HTTPStatus

import allure
import pytest

from tests.api.schemas.user_schema import UserUpdate, UserResponse


@allure.epic("API Tests")
@allure.feature("Users API")
@allure.story("PUT /users/{id}")
@pytest.mark.api
class TestUpdateUser:

    @allure.title("Обновить существующего пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_update_user_success(self, users_client):
        user_id = 2
        updated_data = UserUpdate(name="Updated Name", job="Senior QA")
        
        response = users_client.update_user(user_id, updated_data)

        assert response.status_code == HTTPStatus.OK
        
        updated = UserResponse(**response.json())
        assert updated.name == updated_data.name
        assert updated.job == updated_data.job
        assert updated.updatedAt

    @allure.title("Обновить пользователя с пустыми данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_update_user_empty_data(self, users_client):
        response = users_client.update_user_raw(2, {"name": "", "job": ""})
        
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]

    @allure.title("Обновить несуществующего пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_update_nonexistent_user(self, users_client):
        updated_data = UserUpdate(name="Test", job="Test")
        response = users_client.update_user(99999, updated_data)
        
        assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]

    @allure.title("Обновить пользователя с валидными данными (параметризация)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "user_id,name,job",
        [
            (1, "John Smith", "Developer"),
            (2, "Jane Doe", "Designer"),
            (3, "Bob Johnson", "Manager"),
        ],
        ids=["user_1", "user_2", "user_3"],
    )
    def test_update_different_users(
        self, users_client, user_id: int, name: str, job: str
    ):
        updated_data = UserUpdate(name=name, job=job)
        response = users_client.update_user(user_id, updated_data)

        assert response.status_code == HTTPStatus.OK
        updated = UserResponse(**response.json())
        assert updated.name == name
        assert updated.job == job
