import allure
from allure_commons.types import Severity
import pytest

from src.pages.main_page import MainPage


PAPER_URL = "https://arxiv.org/abs/hep-th/9912012"
PAPER_ID = "hep-th/9912012"
BAD_ID = "hep-th/000000000000"
MISWRITTEN_ID = "hep-th/99120120000000000"


@allure.tag("UI")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("main page")
@allure.title("Main page")
def test_main(setup_browser):
    page = MainPage()
    page.open()


@allure.tag("UI")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("simple search")
@allure.story("search by paper id")
@allure.title("Simple search directs straight to paper when given its id")
@pytest.mark.parametrize("query", [PAPER_ID, BAD_ID, MISWRITTEN_ID])
def test_search_by_id(setup_browser, query):
    page = MainPage()
    page.open()

    page.type_search_query(query)
    page.search()

    if query == BAD_ID:
        page.should_not_recognize_article_id()
    else:
        page.should_be_at_url(PAPER_URL)
