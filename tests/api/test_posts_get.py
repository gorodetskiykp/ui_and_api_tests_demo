from http import HTTPStatus

import allure
import pytest
from pydantic import ValidationError

from tests.api.schemas.post_schema import Comment, PostListItem


@allure.epic("API Tests")
@allure.feature("Posts API")
@allure.story("GET /posts")
@pytest.mark.api
class TestGetPosts:
    @allure.title("Получить список постов")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_get_posts_list(self, posts_client):
        response = posts_client.get_posts()

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        # Валидация через Pydantic
        posts = [PostListItem(**item) for item in data]
        assert all(post.id > 0 for post in posts)
        assert all(post.user_id > 0 for post in posts)

    @allure.title("Получить список постов с лимитом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize("limit", [1, 5, 10])
    def test_get_posts_with_limit(self, posts_client, limit: int):
        response = posts_client.get_posts(limit=limit)

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert len(data) == limit

    @allure.title("Получить пост по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.parametrize("post_id", [1, 5, 10])
    def test_get_post_by_id(self, posts_client, post_id: int):
        response = posts_client.get_post_by_id(post_id)

        assert response.status_code == HTTPStatus.OK

        try:
            post = PostListItem(**response.json())
            assert post.id == post_id
            assert post.title
            assert post.body
            assert post.user_id > 0
        except ValidationError as e:
            pytest.fail(f"Validation error: {e}")

    @allure.title("Получить несуществующий пост")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_get_nonexistent_post(self, posts_client):
        response = posts_client.get_post_by_id(99999)
        assert response.status_code == HTTPStatus.NOT_FOUND

    @allure.title("Получить комментарии к посту")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_get_comments_for_post(self, posts_client):
        response = posts_client.get_comments_for_post(1)

        assert response.status_code == HTTPStatus.OK

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

        comments = [Comment(**item) for item in data]
        assert all(c.post_id == 1 for c in comments)
        assert all(c.email for c in comments)
