from selene import browser, be
from appium.webdriver.common.appiumby import AppiumBy
import allure
from allure_commons.types import Severity


XPATH_THREE_DOTS = ("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android"
                    ".widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                    "android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout[1]/"
                    "android.view.ViewGroup/android.support.v7.widget.av/android.widget.ImageView")
XPATH_SETTINGS = ("/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget."
                  "ListView/android.widget.LinearLayout[1]/android.widget.RelativeLayout/android."
                  "widget.TextView")
XPATH_SETTINGS_HEADING = ("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android"
                          ".widget.FrameLayout/android.widget.LinearLayout/android.view.ViewGroup/"
                          "android.widget.TextView")
XPATH_SEARCH = ("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget."
                "FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view."
                "ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout[1]/android.view."
                "ViewGroup/android.support.v7.widget.av/android.widget.TextView")
XPATH_SEARCH_FIELD = ("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android."
                      "widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/"
                      "android.view.ViewGroup/android.widget.LinearLayout/android.widget."
                      "FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android."
                      "widget.LinearLayout/android.widget.RelativeLayout/android.widget.EditText")


@allure.tag("Mobile")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("settings")
@allure.title("the settings page should open")
def test_settings_opens(setup_browser):
    with allure.step("tap the 'NOT NOW' button when asked to donate"):
        browser.element((AppiumBy.ID, "android:id/button2")).click()
    with allure.step("tap the three dots in the upper right corner"):
        browser.element((AppiumBy.XPATH, XPATH_THREE_DOTS)).click()
    with allure.step("select 'settings' from the dropdown menu"):
        browser.element((AppiumBy.XPATH, XPATH_SETTINGS)).click()
    with allure.step("the settings page should open and its heading should be present"):
        browser.element((AppiumBy.XPATH, XPATH_SETTINGS_HEADING)).should(be.present)


@allure.tag("Mobile")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("settings")
@allure.title("the search field should work")
def test_settings_opens(setup_browser):
    with allure.step("tap the 'NOT NOW' button when asked to donate"):
        browser.element((AppiumBy.ID, "android:id/button2")).click()
    with allure.step("tap search icon at the top of the screen"):
        browser.element((AppiumBy.XPATH, XPATH_SEARCH)).click()
    with allure.step("type 'electron' in the search field"):
        browser.element((AppiumBy.XPATH, XPATH_SEARCH_FIELD)).type("electron")

    # ...it was at this point that the free plan expired
