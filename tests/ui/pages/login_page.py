import allure
from playwright.sync_api import Page, Locator, expect

from tests.ui.pages.base_page import BasePage


class LoginPage(BasePage):

    URL = "/login"
    USERNAME_FIELD: str = "#username"
    PASSWORD_FIELD: str = "#password"
    LOGIN_BUTTON: str = "button[type='submit']"
    FLASH_MESSAGE: str = "#flash"
    SECURE_AREA_HEADING: str = "h2.subheader"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input: Locator = page.locator(self.USERNAME_FIELD)
        self.password_input: Locator = page.locator(self.PASSWORD_FIELD)
        self.login_btn: Locator = page.locator(self.LOGIN_BUTTON)
        self.flash: Locator = page.locator(self.FLASH_MESSAGE)
        self.secure_heading: Locator = page.locator(self.SECURE_AREA_HEADING)


    @allure.step("Открыть страницу логина")
    def open_login_page(self) -> "LoginPage":
        self.open(self.URL)
        return self

    @allure.step("Ввести логин: {username}")
    def enter_username(self, username: str) -> "LoginPage":
        self.fill(self.username_input, username)
        return self

    @allure.step("Ввести пароль")
    def enter_password(self, password: str) -> "LoginPage":
        self.fill(self.password_input, password)
        return self

    @allure.step("Нажать кнопку входа")
    def click_login(self) -> None:
        self.click(self.login_btn)

    def login(self, username: str, password: str) -> None:
        """Полный сценарий логина."""
        self.enter_username(username).enter_password(password).click_login()

    def get_flash_message(self) -> str:
        self.wait_for_element(self.flash)
        return self.flash.inner_text().strip()

    def is_flash_success(self) -> bool:
        return "success" in self.flash.get_attribute("class") or ""

    @allure.step("Проверить успешный вход")
    def expect_successful_login(self) -> None:
        self.wait_for_url("**/secure")
        expect(self.secure_heading).to_contain_text("Welcome")

    @allure.step("Проверить сообщение об ошибке: {expected_text}")
    def expect_error_message(self, expected_text: str) -> None:
        expect(self.flash).to_contain_text(expected_text)
