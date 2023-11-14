import sys
from io import BytesIO

import pytest
import allure
from allure_commons.types import Severity, AttachmentType
import requests
from lxml import etree, html
import feedparser

from tests.conftest import QUERY_XSD


NAME = "all:electron"
BAD_NAME = "all:gibberishgibberishgibberish"
ID = "hep-ex/0307015"
FULL_ID = "http://arxiv.org/abs/hep-ex/0307015v1"

# test  where 400 = {'bozo': False, 'entries': [{'id': 'http://arxiv.org/api/errors#start_must_be_an_integer', 'guidislink': True, 'link': 'http://arxiv.org/api/errors#start_must_be_an_integer', 'title': 'Error', 'title_detail': {'type': 'text/plain', 'language': None, 'base': 'http://export.arxiv.org/api/query?search_query=all:electron&id_list=&max_results=20&start=', 'value': 'Error'}, 'summary': 'start must be an integer', 'summary_detail': {'type': 'text/plain', 'language': None, 'base': 'http://export.arxiv.org/api/query?search_query=all:electron&id_list=&max_results=20&start=', 'value': 'start must be an integer'}, 'updated': '2023-11-14T00:00:00-05:00', 'updated_parsed': time.struct_time(tm_year=2023, tm_mon=11, tm_mday=14, tm_hour=5, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=318, tm_isdst=0), 'links': [{'href': 'http://arxiv.org/api/errors#start_must_be_an_integer', 'rel': 'alternate', 'type': 'text/html'}], 'authors': [{'name': 'arXiv api core'}], 'author_detail': {'name': 'arXiv api core'}, 'author': 'arXiv api core'}], 'feed': {'links': [{'href': 'http://arxiv.org/api/query?search_query%3Dall%3Aelectron%26id_list%3D%26start%3D%26max_results%3D20', 'rel': 'self', 'type': 'application/atom+xml'}], 'title': 'ArXiv Query: search_query=all:electron&amp;id_list=&amp;start=&amp;max_results=20', 'title_detail': {'type': 'text/html', 'language': None, 'base': 'http://export.arxiv.org/api/query?search_query=all:electron&id_list=&max_results=20&start=', 'value': 'ArXiv Query: search_query=all:electron&amp;id_list=&amp;start=&amp;max_results=20'}, 'id': 'http://arxiv.org/api/cCXdrLQOXS1D388sED21M1tqWFc', 'guidislink': True, 'link': 'http://arxiv.org/api/cCXdrLQOXS1D388sED21M1tqWFc', 'updated': '2023-11-14T00:00:00-05:00', 'updated_parsed': time.struct_time(tm_year=2023, tm_mon=11, tm_mday=14, tm_hour=5, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=318, tm_isdst=0), 'opensearch_totalresults': '1', 'opensearch_startindex': '0', 'opensearch_itemsperpage': '1'}, 'headers': {'date': 'Tue, 14 Nov 2023 07:10:40 GMT', 'server': 'Apache', 'access-control-allow-origin': '*', 'vary': 'Accept-Encoding,User-Agent', 'content-encoding': 'gzip', 'content-length': '526', 'connection': 'close', 'content-type': 'application/atom+xml; charset=UTF-8'}, 'href': 'http://export.arxiv.org/api/query?search_query=all:electron&id_list=&max_results=20&start=', 'status': 400, 'encoding': 'UTF-8', 'version': 'atom10', 'namespaces': {'': 'http://www.w3.org/2005/Atom', 'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}}.status


def query(name="", id=None, max_res=None, start=None):
    url = "http://export.arxiv.org/api/query?"
    url += "search_query=" + name
    if id:
        url += "&id_list=" + id
    if max_res:
        url += "&max_results=" + max_res
    if start:
        url += "&start=" + start
    return feedparser.parse(url)


def attach_code(code, name="status code"):
    allure.attach(str(code), name=name, attachment_type=AttachmentType.TEXT)


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
        response = query(name=NAME, max_res=str(max_res))
        attach_code(response.status)

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
        response = query(name=NAME, start="0", max_res="1")
        attach_code(response.status, name="first request status")

    with allure.step("send second request"):
        response1 = query(name=NAME, start="1", max_res="1")
        attach_code(response.status, name="second request status")

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
        response = query(name=NAME, start="-1", max_res="1")
        attach_code()

    with allure.step("check status code"):
        assert response.status == 400


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query")
@allure.title("The id_list parameter should work")
def test_id_list():
    with allure.step("send the request"):
        response = query(id=ID)

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
        response = query(name=BAD_NAME, id=ID)

    with allure.step("check status code"):
        assert response.status == 200
    with allure.step("check that response is empty"):
        assert len(response.entries) == 0
