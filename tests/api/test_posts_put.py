from http import HTTPStatus

import allure
import pytest

from tests.api.schemas.post_schema import PostResponse, PostUpdate


@allure.epic("API Tests")
@allure.feature("Posts API")
@allure.story("PUT /posts/{id}")
@pytest.mark.api
class TestUpdatePost:
    @allure.title("Обновить существующий пост")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_update_post_success(self, posts_client):
        post_id = 1
        updated_data = PostUpdate(
            title="Updated Title",
            body="Updated body content",
            user_id=1,
        )

        response = posts_client.update_post(post_id, updated_data)

        assert response.status_code == HTTPStatus.OK

        updated = PostResponse(**response.json())
        assert updated.id == post_id
        assert updated.title == updated_data.title
        assert updated.body == updated_data.body
        assert updated.user_id == updated_data.user_id

    @allure.title("Обновить разные посты (параметризация)")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "post_id,title,body,user_id",
        [
            (1, "First Post Updated", "New body 1", 1),
            (2, "Second Post Updated", "New body 2", 2),
            (3, "Third Post Updated", "New body 3", 3),
        ],
        ids=["post_1", "post_2", "post_3"],
    )
    def test_update_different_posts(self, posts_client, post_id: int, title: str, body: str, user_id: int):
        updated_data = PostUpdate(title=title, body=body, user_id=user_id)
        response = posts_client.update_post(post_id, updated_data)

        assert response.status_code == HTTPStatus.OK
        updated = PostResponse(**response.json())
        assert updated.title == title
        assert updated.body == body
        assert updated.user_id == user_id

    @allure.title("Обновить пост с пустыми данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_update_post_empty_data(self, posts_client):
        response = posts_client.update_post_raw(1, {"title": "", "body": "", "userId": 1})

        assert response.status_code in [HTTPStatus.OK, HTTPStatus.BAD_REQUEST]

    @allure.title("Обновить несуществующий пост")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_update_nonexistent_post(self, posts_client):
        updated_data = PostUpdate(title="Test", body="Test", user_id=1)
        response = posts_client.update_post(99999, updated_data)

        assert response.status_code in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]
