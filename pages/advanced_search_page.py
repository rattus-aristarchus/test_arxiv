from selene import browser, have, command


class AdvancedSearchPage:

    def __init__(self):
        self.url = "https://arxiv.org/search/advanced"

    def open(self):
        browser.open(self.url)
        browser.all("[id^=google_ads][id$=container__]").with_(timeout=10).wait_until(
            have.size_greater_than_or_equal(3)
        )
        browser.all('[id^=google_ads][id$=container__]').perform(command.js.remove)
