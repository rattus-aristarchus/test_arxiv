import sys
from io import BytesIO

import pytest
import allure
from allure_commons.types import Severity
import requests
from lxml import etree, html
import feedparser

from tests.conftest import QUERY_XSD


QUERY = "http://export.arxiv.org/api/query?"
BY_NAME = "search_query="
BY_ID = "&id_list="
MAX_RES = "&max_results="
START = "&start="

NAME = "all:electron"
BAD_NAME = "all:gibberishgibberishgibberish"
ID = "hep-ex/0307015"
FULL_ID = "http://arxiv.org/abs/hep-ex/0307015v1"

"""
@allure.tag("API")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("Search query response should be well-formed")
def test_search_query():
    with allure.step("prepare schema"):
        schema_doc = etree.parse(QUERY_XSD)
        schema = etree.XMLSchema(schema_doc)

    with allure.step("send a request"):
        url = QUERY + BY_NAME + NAME
        response = requests.get(url)
    with allure.step("parse the response"):
        xml_doc = etree.parse(BytesIO(bytes(response.text, 'utf-8')))

    with allure.step("check status code"):
        assert response.status_code == 200
    with allure.step("validate the xml with the schema"):
        assert schema.validate(xml_doc)
"""


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The max_results parameter should work")
@pytest.mark.parametrize("max_res", [20, 0, sys.maxsize])
# for performance reasons, arxiv's maximum number of results
# returned from a single call (max_results) is limited to 30000,
# and they frown upon calls of over 1000
def test_query_max_results(max_res):
    if max_res == sys.maxsize:
        expected_code = 400
    else:
        expected_code = 200

    with allure.step("send a request"):
        url = QUERY + BY_NAME + NAME + MAX_RES + str(max_res)
        response = feedparser.parse(url)

    with allure.step("check status code"):
        assert response.status == expected_code
    with allure.step("check there are no more results than max_results"):
        assert len(response.entries) <= max_res


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The start parameter should work")
def test_query_start():
    with allure.step("send first request"):
        url0 = QUERY + BY_NAME + NAME + START + "0" + MAX_RES + "1"
        response = feedparser.parse(url0)

    with allure.step("send second request"):
        url1 = QUERY + BY_NAME + NAME + START + "1" + MAX_RES + "1"
        response1 = feedparser.parse(url1)

    with allure.step("check status code for first request"):
        assert response.status == 200
    with allure.step("check status code for second request"):
        assert response1.status == 200
    if len(response.entries) > 0 and len(response.entries) > 0:
        with allure.step("make sure the returned entities are different"):
            assert not response.entries[0].id == response1.entries[0].id


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The start parameter should not accept negative numbers")
def test_query_start():
    with allure.step("send the request"):
        url = QUERY + BY_NAME + NAME + START + "-1" + MAX_RES + "1"
        response = feedparser.parse(url)

    with allure.step("check status code"):
        assert response.status == 400


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The id_list parameter should work")
def test_id_list():
    with allure.step("send the request"):
        url = QUERY + BY_NAME + BY_ID + ID
        response = feedparser.parse(url)

    with allure.step("check status code"):
        assert response.status == 200
    with allure.step("check that response has one entry"):
        assert len(response.entries) == 1
    with allure.step("check the retrieved entity"):
        assert response.entries[0].id == FULL_ID


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The id_list parameter should work with query by name")
def test_id_list_with_name():
    with allure.step("send the request"):
        url = QUERY + BY_NAME + BAD_NAME + BY_ID + ID
        response = feedparser.parse(url)

    with allure.step("check status code"):
        assert response.status == 200
    with allure.step("check that response is empty"):
        assert len(response.entries) == 0
