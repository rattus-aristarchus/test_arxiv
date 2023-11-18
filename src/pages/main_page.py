import allure

from src.pages.page import Page


class MainPage(Page):

    def __init__(self):
        self.url = "https://arxiv.org"

    @allure.step("open the https://arxiv.org page")
    def open(self):
        self.open_url(self.url)
