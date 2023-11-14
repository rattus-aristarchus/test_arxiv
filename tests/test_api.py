import sys
from io import BytesIO

import pytest
import allure
from allure_commons.types import Severity
import requests
from lxml import etree
import feedparser

from tests.conftest import QUERY_XSD


API_URL = "http://export.arxiv.org/api/"
QUERY_MAX_RES = "query?search_query=all:electron&max_results="


@allure.tag("API")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("Search query response shoudl be well-formed")
def test_search_query():
    schema_doc = etree.parse(QUERY_XSD)
    schema = etree.XMLSchema(schema_doc)
    url = API_URL + "query?search_query=all:electron"

    response = requests.get(url)
    xml_doc = etree.parse(BytesIO(bytes(response.text, 'utf-8')))

    assert response.status_code == 200
    assert schema.validate(xml_doc)


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The max_results parameter should work")
@pytest.mark.parametrize("max_res", [20, 0, sys.maxsize])
def test_query_max_results(max_res):
    url = API_URL + QUERY_MAX_RES + str(max_res)

    response = feedparser.parse(url)

    assert response.status == 200
    assert len(response.entries) <= max_res
