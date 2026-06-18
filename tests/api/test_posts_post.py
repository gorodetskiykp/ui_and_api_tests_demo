from http import HTTPStatus

import allure
import pytest
from faker import Faker

from tests.api.schemas.post_schema import PostCreate, PostResponse

fake = Faker()


@allure.epic("API Tests")
@allure.feature("Posts API")
@allure.story("POST /posts")
@pytest.mark.api
class TestCreatePost:
    @allure.title("Создать пост с валидными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_create_post_success(self, posts_client, sample_post_data):
        post = PostCreate(**sample_post_data)
        response = posts_client.create_post(post)

        assert response.status_code == HTTPStatus.CREATED

        created = PostResponse(**response.json())
        assert created.title == post.title
        assert created.body == post.body
        assert created.user_id == post.user_id
        assert created.id > 0

    @allure.title("Создать пост с русскими данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_post_russian_locale(self, posts_client):
        fake_ru = Faker("ru_RU")
        post = PostCreate(
            title=fake_ru.sentence(),
            body=fake_ru.paragraph(),
            user_id=1,
        )

        response = posts_client.create_post(post)

        assert response.status_code == HTTPStatus.CREATED
        created = PostResponse(**response.json())
        assert created.title == post.title

    @allure.title("Создать пост с различными данными (параметризация)")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "title,body,user_id",
        [
            pytest.param("Simple Title", "Simple body text", 1, id="simple"),
            pytest.param("Title with numbers 123", "Body with symbols !@#", 2, id="with_symbols"),
            pytest.param("Длинный заголовок", "Длинное тело поста", 3, id="russian"),
            pytest.param(fake.sentence(), fake.paragraph(), 4, id="faker_generated"),
        ],
    )
    def test_create_post_various_data(self, posts_client, title: str, body: str, user_id: int):
        post = PostCreate(title=title, body=body, user_id=user_id)
        response = posts_client.create_post(post)

        assert response.status_code == HTTPStatus.CREATED
        created = PostResponse(**response.json())
        assert created.title == title
        assert created.body == body
        assert created.user_id == user_id

    @allure.title("Создать несколько постов последовательно")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_multiple_posts(self, posts_client, multiple_posts_data):
        created_posts = []

        for post_data in multiple_posts_data:
            post = PostCreate(**post_data)
            response = posts_client.create_post(post)

            assert response.status_code == HTTPStatus.CREATED
            created = PostResponse(**response.json())
            created_posts.append(created)

        ids = [p.id for p in created_posts]
        assert len(ids) == len(set(ids)), "Все ID должны быть уникальными"

    @allure.title("Создать пост с пустым заголовком")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_create_post_empty_title(self, posts_client):
        response = posts_client.create_post_raw(
            {
                "title": "",
                "body": "Some body",
                "userId": 1,
            }
        )

        assert response.status_code in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]

    @allure.title("Создать пост без тела запроса")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_create_post_no_body(self, posts_client):
        response = posts_client.post("/posts", json_data=None)
        assert response.status_code in [HTTPStatus.CREATED, HTTPStatus.BAD_REQUEST]

    @allure.title("Создать пост с невалидным JSON")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    def test_create_post_invalid_json(self, posts_client):
        response = posts_client.post(
            "/posts",
            content=b'{"title": "Test", "body":',
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST
