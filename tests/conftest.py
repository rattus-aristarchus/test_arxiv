import pytest
from selene import browser
from selenium import webdriver


@pytest.fixture(autouse=True)
def setup_browser():
    browser.config.driver = webdriver.Chrome()
    browser.config.window_width = 1600
    browser.config.window_height = 1200

    yield

    browser.quit()
