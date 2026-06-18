from typing import Any, Dict, Optional

import allure
import httpx
from loguru import logger


class BaseAPIClient:

    def __init__(self, base_url: str, timeout: float = 30.0):
        self.base_url = base_url
        self.timeout = timeout
        self.client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )
        logger.info(f"API клиент создан: {base_url}")

    @allure.step("GET {endpoint}")
    def get(
        self,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> httpx.Response:
        logger.info(f"GET {self.base_url}{endpoint}")
        response = self.client.get(endpoint, params=params, **kwargs)
        self._log_response(response)
        return response

    @allure.step("POST {endpoint}")
    def post(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> httpx.Response:
        logger.info(f"POST {self.base_url}{endpoint}")
        logger.debug(f"Request body: {json_data}")
        response = self.client.post(endpoint, json=json_data, **kwargs)
        self._log_response(response)
        return response

    @allure.step("PUT {endpoint}")
    def put(
        self,
        endpoint: str,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> httpx.Response:
        logger.info(f"PUT {self.base_url}{endpoint}")
        logger.debug(f"Request body: {json_data}")
        response = self.client.put(endpoint, json=json_data, **kwargs)
        self._log_response(response)
        return response

    @allure.step("DELETE {endpoint}")
    def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        logger.info(f"DELETE {self.base_url}{endpoint}")
        response = self.client.delete(endpoint, **kwargs)
        self._log_response(response)
        return response

    def _log_response(self, response: httpx.Response) -> None:
        logger.info(f"Response: {response.status_code}")
        logger.debug(f"Response body: {response.text}")

        allure.attach(
            f"{response.request.method} {response.request.url}",
            name="Request",
            attachment_type=allure.attachment_type.TEXT,
        )
        allure.attach(
            f"Status: {response.status_code}\n\n{response.text}",
            name="Response",
            attachment_type=allure.attachment_type.TEXT,
        )

    def close(self) -> None:
        self.client.close()
        logger.info("API клиент закрыт")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
