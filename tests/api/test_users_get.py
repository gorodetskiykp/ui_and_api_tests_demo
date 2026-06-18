from http import HTTPStatus

import allure
import pytest
from pydantic import ValidationError

from tests.api.schemas.user_schema import UserListResponse, SingleUserResponse


@allure.epic("API Tests")
@allure.feature("Users API")
@allure.story("GET /users")
@pytest.mark.api
class TestGetUsers:

    @allure.title("Получить список пользователей (страница 1)")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_get_users_list(self, users_client):
        response = users_client.get_users(page=1)

        assert response.status_code == HTTPStatus.OK
        
        try:
            data = UserListResponse(**response.json())
            assert data.page == 1
            assert data.per_page > 0
            assert data.total > 0
            assert len(data.data) > 0
            assert data.data[0].email
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    @allure.title("Получить пользователя по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("user_id", [1, 2, 3])
    def test_get_user_by_id(self, users_client, user_id: int):
        response = users_client.get_user_by_id(user_id)

        assert response.status_code == HTTPStatus.OK
        
        try:
            data = SingleUserResponse(**response.json())
            assert data.data.id == user_id
            assert data.data.email
            assert data.data.first_name
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    @allure.title("Получить несуществующего пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_nonexistent_user(self, users_client):
        response = users_client.get_user_by_id(99999)
        assert response.status_code == HTTPStatus.NOT_FOUND
