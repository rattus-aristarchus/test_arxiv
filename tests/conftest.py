import os

import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        help="Браузер для запуска тестов",
        choices=["firefox", "chrome"],
        default="chrome"
    )
    parser.addoption(
        "--browser_version",
        help="Версия браузера",
        default="100.0"
    )


@pytest.fixture(scope="session")
def setup_browser(request):
    browser.config.window_width = 1600
    browser.config.window_height = 1200
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")

    login = os.getenv('LOGIN')
    pwd = os.getenv('PASSWORD')

    options = Options()
    selenoid_capabilities = {
        "browserName": browser_name,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)
    driver = webdriver.Remote(
        command_executor=f"https://{login}:{pwd}@selenoid.autotests.cloud/wd/hub",
        options=options
    )

    browser.config.driver = driver

    yield browser

    browser.quit()
