import allure
import pytest
from allure_commons.types import Severity

from src.pages.advanced_search_page import AdvancedSearchPage


QUERY = "electron"
BAD_QUERY = "asdasdlsklalkjasdfljka"
QUERY_ECON = "cycles"
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
        page.results_should_exist()
    elif search_term == BAD_QUERY:
        page.should_not_have_results()


@allure.tag("UI")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search by field")
@allure.title("Diacritics should be automatically searched for authors")
def test_diacritics(setup_browser):
    page = AdvancedSearchPage()
    page.open()

    page.fill_search_term(NAME_WO_DIACRITICS)
    page.set_field("author")
    page.search()

    page.results_should_have_author(NAME_WITH_DIACRITICS)


@allure.tag("UI")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search with subject")
@allure.title("All results should have the selected subject tag")
def test_tag_inclusive(setup_browser):
    page = AdvancedSearchPage()
    page.open()

    page.fill_search_term(QUERY)
    page.set_subject("Economics")
    page.set_include_cross_listed()
    page.search()

    page.all_results_should_have_tag("econ")


@allure.tag("UI")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("advanced search")
@allure.story("search with subject")
@allure.issue("https://jira.autotests.cloud", name="HOMEWORK-963")
@allure.title("All results should have only the selected subject tag")
def test_tag_exclusive(setup_browser):
    page = AdvancedSearchPage()
    page.open()

    page.fill_search_term(QUERY_ECON)
    page.set_subject("Economics")
    page.set_exclude_cross_listed()
    page.search()

    page.all_results_should_only_have_tag("econ")
