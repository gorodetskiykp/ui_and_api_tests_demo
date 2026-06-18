import allure
from loguru import logger
from playwright.sync_api import Locator, Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Открыть страницу: {url}")
    def open(self, url: str = "") -> None:
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        logger.info(f"Открытие: {full_url}")
        self.page.goto(full_url, wait_until="domcontentloaded")

    @property
    def base_url(self) -> str:
        from config.settings import settings

        return settings.base_url

    def wait_for_element(self, locator: Locator, timeout: int | None = None) -> None:
        timeout = timeout or self._default_timeout
        locator.wait_for(state="visible", timeout=timeout)

    def wait_for_url(self, url_pattern: str, timeout: int | None = None) -> None:
        self.page.wait_for_url(url_pattern, timeout=timeout or self._default_timeout)

    @property
    def _default_timeout(self) -> int:
        from config.settings import settings

        return settings.timeout

    @allure.step("Клик по элементу")
    def click(self, locator: Locator) -> None:
        self.wait_for_element(locator)
        locator.click()

    @allure.step("Заполнить поле")
    def fill(self, locator: Locator, value: str) -> None:
        self.wait_for_element(locator)
        locator.fill(value)

    @allure.step("Очистить и заполнить поле")
    def clear_and_fill(self, locator: Locator, value: str) -> None:
        self.wait_for_element(locator)
        locator.clear()
        locator.fill(value)

    def get_text(self, locator: Locator) -> str:
        self.wait_for_element(locator)
        return locator.inner_text().strip()

    def is_visible(self, locator: Locator, timeout: int = 3_000) -> bool:
        try:
            locator.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    @allure.step("Скриншот: {name}")
    def take_screenshot(self, name: str) -> bytes:
        screenshot = self.page.screenshot(full_page=True)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot
