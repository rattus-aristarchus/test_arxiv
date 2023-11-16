import os

import pytest

import dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(BASE_DIR, "resources")


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        help="Браузер для запуска тестов",
        choices=["firefox", "chrome"],
        default="chrome"
    )
    parser.addoption(
        "--browser_version",
        help="Версия браузера",
        default="100.0"
    )
