import allure
import pytest
from allure_commons.types import Severity

from src.pages.advanced_search_page import AdvancedSearchPage
from tests.web.conftest import QUERY, BAD_QUERY


@allure.tag("UI")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search by field")
@allure.title("Advanced search works")
@pytest.mark.parametrize("search_term", [QUERY, BAD_QUERY])
def test_works(local_browser, search_term):
    with allure.step("open the advanced search page"):
        page = AdvancedSearchPage()
        page.open()

    with allure.step("fill in the search term"):
        page.fill_search_term(search_term)

    with allure.step("click the search button"):
        page.search()

    if search_term == QUERY:
        with allure.step("results should appear"):
            page.should_have_results()
    elif search_term == BAD_QUERY:
        with allure.step("results should be empty"):
            page.should_not_have_results()


@allure.tag("UI")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search by field")
@allure.title("Diacritics should be automatically searched for authors")
def test_diacritics(setup_browser):
    with allure.step("open the advanced search page"):
        page = AdvancedSearchPage()
        page.open()



