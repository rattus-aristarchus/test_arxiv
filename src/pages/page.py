import allure
from selene import browser, have, command


class Page:

    def open_url(self, url):
        browser.open(url)
        browser.all("[id^=google_ads][id$=container__]").with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)
