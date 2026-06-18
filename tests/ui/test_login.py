import allure
import pytest

from tests.ui.pages.login_page import LoginPage


@allure.epic("UI Tests")
@allure.feature("Авторизация")
@allure.story("Страница логина the-internet.herokuapp.com")
@pytest.mark.ui
class TestLogin:

    @allure.title("Успешный вход с валидными credentials")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_successful_login(self, login_page: LoginPage):
        from config.settings import settings

        login_page.open_login_page()
        login_page.login(settings.valid_username, settings.valid_password)
        login_page.expect_successful_login()

    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_with_invalid_password(self, login_page: LoginPage):
        login_page.open_login_page()
        login_page.login("tomsmith", "WrongPassword")
        login_page.expect_error_message("Your password is invalid!")

    @allure.title("Вход с несуществующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    def test_login_with_invalid_username(self, login_page: LoginPage):
        login_page.open_login_page()
        login_page.login("unknown_user", "SuperSecretPassword!")
        login_page.expect_error_message("Your username is invalid!")

    @allure.title("Вход с пустыми полями")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("username", "password", "expected_error"),
        [
            pytest.param("", "", "Your username is invalid!", id="both_empty"),
            pytest.param("", "SuperSecretPassword!", "Your username is invalid!", id="empty_username"),
            pytest.param("tomsmith", "", "Your password is invalid!", id="empty_password"),
        ],
    )
    def test_login_with_empty_fields(
        self,
        login_page: LoginPage,
        username: str,
        password: str,
        expected_error: str,
    ):
        login_page.open_login_page()
        login_page.login(username, password)
        login_page.expect_error_message(expected_error)

    @allure.title("Проверка доступности формы логина")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.smoke
    def test_login_form_is_displayed(self, login_page: LoginPage):
        login_page.open_login_page()
        assert login_page.is_visible(login_page.username_input)
        assert login_page.is_visible(login_page.password_input)
        assert login_page.is_visible(login_page.login_btn)


    @allure.title("Логин с пробелами в начале/конце")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("username", "password", "expected_error"),
        [
            pytest.param(
                " tomsmith", "SuperSecretPassword!", 
                "Your username is invalid!", 
                id="leading_space_in_username"
            ),
            pytest.param(
                "tomsmith ", "SuperSecretPassword!", 
                "Your username is invalid!", 
                id="trailing_space_in_username"
            ),
            pytest.param(
                " tomsmith ", "SuperSecretPassword!", 
                "Your username is invalid!", 
                id="both_spaces_in_username"
            ),
            pytest.param(
                "tomsmith", " SuperSecretPassword!", 
                "Your password is invalid!", 
                id="leading_space_in_password"
            ),
            pytest.param(
                "tomsmith", "SuperSecretPassword! ", 
                "Your password is invalid!", 
                id="trailing_space_in_password"
            ),
        ],
    )
    def test_login_with_spaces(
        self,
        login_page: LoginPage,
        username: str,
        password: str,
        expected_error: str,
    ):
        login_page.open_login_page()
        login_page.login(username, password)
        login_page.expect_error_message(expected_error)


    @allure.title("Логин с неверным регистром")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.parametrize(
        ("username", "password", "expected_error"),
        [
            pytest.param(
                "TomSmith", "SuperSecretPassword!", 
                "Your username is invalid!", 
                id="username_title_case"
            ),
            pytest.param(
                "TOMSMITH", "SuperSecretPassword!", 
                "Your username is invalid!", 
                id="username_uppercase"
            ),
            pytest.param(
                "tomsmith", "supersecretpassword!", 
                "Your password is invalid!", 
                id="password_lowercase"
            ),
            pytest.param(
                "tomsmith", "SUPERSECRETPASSWORD!", 
                "Your password is invalid!", 
                id="password_uppercase"
            ),
        ],
    )
    def test_login_with_wrong_case(
        self,
        login_page: LoginPage,
        username: str,
        password: str,
        expected_error: str,
    ):
        login_page.open_login_page()
        login_page.login(username, password)
        login_page.expect_error_message(expected_error)
