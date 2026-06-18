from typing import Any

import httpx
from loguru import logger

from tests.api.clients.base_client import BaseAPIClient
from tests.api.schemas.post_schema import PostCreate, PostUpdate


class PostsClient(BaseAPIClient):
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com", timeout: float = 30.0):
        super().__init__(base_url, timeout)

    def get_posts(self, limit: int | None = None) -> httpx.Response:
        params = {"_limit": limit} if limit else None
        return self.get("/posts", params=params)

    def get_post_by_id(self, post_id: int) -> httpx.Response:
        return self.get(f"/posts/{post_id}")

    def get_comments_for_post(self, post_id: int) -> httpx.Response:
        return self.get(f"/posts/{post_id}/comments")

    def create_post(self, post_data: PostCreate) -> httpx.Response:
        logger.info(f"Создание поста: {post_data.title[:50]}...")
        return self.post("/posts", json_data=post_data.model_dump(by_alias=True))

    def create_post_raw(self, data: dict[str, Any]) -> httpx.Response:
        logger.info(f"Создание поста с сырыми данными: {data}")
        return self.post("/posts", json_data=data)

    def update_post(self, post_id: int, post_data: PostUpdate) -> httpx.Response:
        logger.info(f"Обновление поста {post_id}: {post_data.title[:50]}...")
        return self.put(f"/posts/{post_id}", json_data=post_data.model_dump(by_alias=True))

    def update_post_raw(self, post_id: int, data: dict[str, Any]) -> httpx.Response:
        logger.info(f"Обновление поста {post_id} с сырыми данными: {data}")
        return self.put(f"/posts/{post_id}", json_data=data)

    def delete_post(self, post_id: int) -> httpx.Response:
        logger.info(f"Удаление поста {post_id}")
        return self.delete(f"/posts/{post_id}")
