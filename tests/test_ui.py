import pytest
from pages.main_page import MainPage


def test_main():
    page = MainPage()
    page.open()
