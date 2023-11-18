from selene import browser, have, be, by
from selene.support.shared.jquery_style import s
import allure

from src.pages.page import Page


FIELD_IDS = {
    "author": '[value="author"]',
    "title": '[value="title"]'
}


class AdvancedSearchPage(Page):

    def __init__(self):
        self.url = "https://arxiv.org/search/advanced"

    @allure.step("open the https://arxiv.org/search/advanced page")
    def open(self):
        self.open_url(self.url)

    @allure.step("type {search_string} in the 'search term' field number {term_no}")
    def fill_search_term(self, search_string, term_no=0):
        term_id = f"#terms-{term_no}-term"
        browser.element(term_id).type(search_string)

    def set_field(self, field, term_no=0):
        dropdown_id = f"#terms-{term_no}-field"
        browser.element(dropdown_id).click()
        browser.element(dropdown_id).element(FIELD_IDS[field]).click()

    @allure.step("click the 'search' button")
    def search(self):
        browser.element(".button.is-link.is-medium").click()

    @allure.step("the results page should have results")
    def should_have_results(self):
        browser.element(".arxiv-result").should(be.existing)

    @allure.step("there should be no results on the results page")
    def should_not_have_results(self):
        browser.element(".arxiv-result").should(be.absent)

    @allure.step("any of the 'authors' field of results should contain {author}")
    def results_should_have_author(self, author):
        browser.element(".authors").should(have.text(author))
