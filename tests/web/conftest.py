import os

import pytest
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def local_browser():
    browser.config.driver = webdriver.Chrome()
    browser.config.window_width = 1600
    browser.config.window_height = 1200

    yield

    browser.close()


@pytest.fixture(scope="function")
def setup_browser(request):
    browser.config.window_width = 1600
    browser.config.window_height = 1200
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser_version")

    login = os.getenv('SELENOID_LOGIN')
    pwd = os.getenv('SELENOID_PASSWORD')

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
