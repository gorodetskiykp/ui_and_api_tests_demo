import pytest
from faker import Faker

from tests.api.clients.users_client import UsersClient

fake = Faker()


@pytest.fixture(scope="session")
def users_client() -> UsersClient:
    client = UsersClient()
    yield client
    client.close()


@pytest.fixture
def sample_user_data() -> dict:
    return {
        "name": fake.name(),
        "job": fake.job(),
    }


@pytest.fixture
def random_user_data() -> dict:
    return {
        "name": fake.first_name(),
        "job": fake.job(),
    }


@pytest.fixture
def multiple_users_data():
    return [{"name": fake.name(), "job": fake.job()} for _ in range(5)]
