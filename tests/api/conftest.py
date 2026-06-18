import pytest
from faker import Faker

from tests.api.clients.posts_client import PostsClient

fake = Faker()


@pytest.fixture(scope="session")
def posts_client() -> PostsClient:
    client = PostsClient()
    yield client
    client.close()


@pytest.fixture
def sample_post_data() -> dict:
    return {
        "title": fake.sentence(nb_words=6),
        "body": fake.paragraph(nb_sentences=3),
        "user_id": fake.random_int(min=1, max=10),
    }


@pytest.fixture
def multiple_posts_data():
    return [
        {
            "title": fake.sentence(nb_words=6),
            "body": fake.paragraph(nb_sentences=3),
            "user_id": fake.random_int(min=1, max=10),
        }
        for _ in range(5)
    ]
