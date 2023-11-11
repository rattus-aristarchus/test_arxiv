from pages.main_page import MainPage


def test_main(setup_browser):
    page = MainPage()
    page.open()
