from selene import browser
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
        "app": "bs://4596d0720ffc4b92d7fd6f5ba399273c71eac54c",

        # Set other BrowserStack capabilities
        'bstack:options': {
            "projectName": "Arxiv Mobile",
            "buildName": "arxiv-mobile-build-1",
            "sessionName": "arxiv first_test",

            # Set your access credentials
            "userName": os.getenv("BROWSERSTACK_LOGIN"),
            "accessKey": os.getenv("BROWSERSTACK_PASSWORD")
        }
    })

    # Initialize the remote Webdriver using BrowserStack remote URL
    # and options defined above
    driver = webdriver.Remote("http://hub.browserstack.com/wd/hub", options=options)

    # версия селена: просто browser.config.driver_options = options

    browser.config.driver = driver

    yield browser

    browser.quit()
