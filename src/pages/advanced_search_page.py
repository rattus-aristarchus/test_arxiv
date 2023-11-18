from selene import browser, have, be, by
from selene.support.shared.jquery_style import s
import allure

from src.pages.page import Page


FIELD_IDS = {
    "author": '[value="author"]',
    "title": '[value="title"]'
}
SUBJECT_IDS = {
    "Economics": "#classification-economics"
}


class AdvancedSearchPage(Page):

    def __init__(self):
        self.url = "https://arxiv.org/search/advanced"

    @allure.step("open the https://arxiv.org/search/advanced page")
    def open(self):
        self.open_url(self.url)

    @allure.step("type {search_string} in the 'search term' input (number {term_no})")
    def fill_search_term(self, search_string, term_no=0):
        term_id = f"#terms-{term_no}-term"
        browser.element(term_id).type(search_string)

    @allure.step("select field {field} for the 'search term' input (number {term_no})")
    def set_field(self, field, term_no=0):
        dropdown_id = f"#terms-{term_no}-field"
        browser.element(dropdown_id).click()
        browser.element(dropdown_id).element(FIELD_IDS[field]).click()

    @allure.step("click the {subject} tick box under 'Subject'")
    def set_subject(self, subject):
        browser.element(SUBJECT_IDS[subject]).click()

    @allure.step("click the 'Include cross-listed papers' radio button under 'Subject'")
    def set_include_cross_listed(self):
        browser.element("#classification-include_cross_list-0").click()

    @allure.step("click the 'Exclude cross-listed papers' radio button under 'Subject'")
    def set_exclude_cross_listed(self):
        browser.element("#classification-include_cross_list-1").click()

    @allure.step("click the 'search' button")
    def search(self):
        browser.element(".button.is-link.is-medium").click()

    @allure.step("the results page should have results")
    def results_should_exist(self):
        browser.element(".arxiv-result").should(be.existing)

    @allure.step("there should be no results on the results page")
    def should_not_have_results(self):
        browser.element(".arxiv-result").should(be.absent)

    # TODO: this should react to any authors field, not just the first one
    @allure.step("any of the 'authors' field of results should contain {author}")
    def results_should_have_author(self, author):
        browser.element(".authors").should(have.text(author))

    @allure.step("all 'tags' fields should have tag {tag}")
    def all_results_should_have_tag(self, tag):
        for element in browser.all(".tags.is-inline-block"):
            element.should(have.text(tag))

    @allure.step("'tags' fields should only have the tag {tag}")
    def all_results_should_only_have_tag(self, tag):
        for tags in browser.all(".tags.is-inline-block"):
            for tag_element in tags.all(".tag.is-small.tooltip.is-tooltip-top"):
                tag_element.should(have.text(tag))
