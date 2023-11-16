from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

import pytest


@pytest.fixture(scope="session")
def setup_browser(request):
    options = UiAutomator2Options().load_capabilities({
        # Specify device and os_version for testing
        "platformName": "android",
        "platformVersion": "9.0",
        "deviceName": "Google Pixel 3",

        # Set URL of the application under test
        "app": "bs://<app-id>",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "First Python project",
            "buildName": "browserstack-build-1",
            "sessionName": "BStack first_test",

            # Set your access credentials
            "userName": os.getenv("BROWSERSTACK_LOGIN"),
            "accessKey": os.getenv("BROWSERSTACK_PASSWORD")
        }
    })

    # Initialize the remote Webdriver using BrowserStack remote URL
    # and options defined above
    driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)

    # версия селена: просто browser.config.driver_options = options

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