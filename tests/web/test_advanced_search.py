import allure
import pytest
from allure_commons.types import Severity

from src.pages.advanced_search_page import AdvancedSearchPage


QUERY = "electron"
BAD_QUERY = "asdasdlsklalkjasdfljka"
NAME_WO_DIACRITICS = "Rontgen"
NAME_WITH_DIACRITICS = "Röntgen"


@allure.tag("UI")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search by field")
@allure.title("Advanced search works")
@pytest.mark.parametrize("search_term", [QUERY, BAD_QUERY])
def test_works(setup_browser, search_term):
    page = AdvancedSearchPage()
    page.open()

    page.fill_search_term(search_term)
    page.search()

    if search_term == QUERY:
        page.should_have_results()
    elif search_term == BAD_QUERY:
        page.should_not_have_results()


@allure.tag("UI")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search by field")
@allure.title("Diacritics should be automatically searched for authors")
def test_diacritics(local_browser):
    page = AdvancedSearchPage()
    page.open()

    page.fill_search_term(NAME_WO_DIACRITICS)
    page.set_field("author")
    page.search()

    page.results_should_have_author(NAME_WITH_DIACRITICS)
