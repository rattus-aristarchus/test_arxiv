import allure
from selene import browser, have, command

import tests.attach as attach


class Page:

    def open_url(self, url):
        browser.open(url)
        browser.all("[id^=google_ads][id$=container__]").with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)

    @allure.step("page url should be {url}")
    def should_be_at_url(self, url):
        attach.add_text(browser, url)
        browser.should(have.url(url))

    @allure.step("should not recognize article identifier")
    def should_not_recognize_article_id(self):
        attach.add_screenshot(browser)
        browser.element("#content").element("h1").should(have.text("not recognized"))
