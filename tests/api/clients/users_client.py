from typing import Any

import httpx
from loguru import logger

from tests.api.clients.base_client import BaseAPIClient
from tests.api.schemas.user_schema import UserCreate, UserUpdate


class UsersClient(BaseAPIClient):

    def __init__(self, base_url: str = "https://reqres.in/api", timeout: float = 30.0):
        super().__init__(base_url, timeout)

    def get_users(self, page: int = 1) -> httpx.Response:
        return self.get("/users", params={"page": page})

    def get_user_by_id(self, user_id: int) -> httpx.Response:
        return self.get(f"/users/{user_id}")

    def create_user(self, user_data: UserCreate) -> httpx.Response:
        logger.info(f"Создание пользователя: {user_data.name}")
        return self.post("/users", json_data=user_data.model_dump())

    def create_user_raw(self, data: dict[str, Any]) -> httpx.Response:
        logger.info(f"Создание пользователя с сырыми данными: {data}")
        return self.post("/users", json_data=data)

    def update_user(self, user_id: int, user_data: UserUpdate) -> httpx.Response:
        logger.info(f"Обновление пользователя {user_id}: {user_data.name}")
        return self.put(f"/users/{user_id}", json_data=user_data.model_dump())

    def update_user_raw(self, user_id: int, data: dict[str, Any]) -> httpx.Response:
        logger.info(f"Обновление пользователя {user_id} с сырыми данными: {data}")
        return self.put(f"/users/{user_id}", json_data=data)

    def delete_user(self, user_id: int) -> httpx.Response:
        logger.info(f"Удаление пользователя {user_id}")
        return self.delete(f"/users/{user_id}")
