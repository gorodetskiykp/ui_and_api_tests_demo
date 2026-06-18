import pluggy
import pytest
from playwright.sync_api import Page

from config.settings import settings
from tests.ui.pages.login_page import LoginPage


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "viewport": {
            "width": settings.viewport_width,
            "height": settings.viewport_height,
        },
        "locale": "ru-RU",
        "timezone_id": "Europe/Moscow",
    }


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(autouse=True)
def _attach_screenshot_on_failure(page: Page, request):
    yield
    if request.node.rep_call and request.node.rep_call.failed:
        screenshot = page.screenshot(full_page=True)
        import allure
        allure.attach(
            screenshot,
            name=f"failure_{request.node.name}",
            attachment_type=allure.attachment_type.PNG,
        )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome: pluggy.Result = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
