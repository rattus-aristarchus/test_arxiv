import allure
from selene import browser, by, have, be

from src.pages.page import Page


class MainPage(Page):

    def __init__(self):
        self.url = "https://arxiv.org"

    @allure.step("open the https://arxiv.org page")
    def open(self):
        self.open_url(self.url)

    @allure.step("type {query} in the search field")
    def type_search_query(self, query):
        browser.element(by.name("query")).type(query)

    @allure.step("click the 'Search' button")
    def search(self):
        browser.element("button.button.is-small.is-cul-darker").click()

