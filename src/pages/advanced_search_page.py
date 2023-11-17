from selene import browser, have, be, by
from selene.support.shared.jquery_style import s

from src.pages.page import Page


class AdvancedSearchPage(Page):

    def __init__(self):
        self.url = "https://arxiv.org/search/advanced"

    def fill_search_term(self, search_string, term_no=0):
        term_id = f"#terms-{term_no}-term"
        browser.element(term_id).type(search_string)

    def set_field(self):
        pass

    def search(self):
        browser.element(".button.is-link.is-medium").click()

    def should_have_results(self):
        browser.element(".arxiv-result").should(be.existing)

    def should_not_have_results(self):
        browser.element(".arxiv-result").should(be.absent)

    def results_should_have_author(self, author):
        browser.element(".authors").should(have.text(author))


