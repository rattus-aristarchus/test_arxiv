import allure
from allure_commons.types import Severity

from src.pages.main_page import MainPage


@allure.tag("UI")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("main page")
@allure.title("Main page should open")
def test_main(setup_browser):
    page = MainPage()
    page.open()




