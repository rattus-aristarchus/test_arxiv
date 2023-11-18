import sys

import pytest
import allure
from allure_commons.types import Severity, AttachmentType
import feedparser


NAME = "all:electron"
BAD_NAME = "all:gibberishgibberishgibberish"
ID = "hep-ex/0307015"
FULL_ID = "http://arxiv.org/abs/hep-ex/0307015v1"


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


@allure.tag("API")
@allure.severity(severity_level=Severity.CRITICAL)
@allure.label("owner", 'lankinma')
@allure.feature("query method")
@allure.title("Query response should be well-formed xml")
def test_search_query():
    with allure.step("send a request"):
        response = query(NAME)
        attach_code(response.status)

    with allure.step("check status code"):
        assert response.status == 200
    with allure.step("make sure the xml is well-formed"):
        assert response.bozo == 0


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query method")
@allure.title("Check acceptable values for max_results")
@pytest.mark.parametrize("max_res", ["20", "0"])
# for performance reasons, arxiv's maximum number of results
# returned from a single call (max_results) is limited to 30000,
# and they frown upon calls of over 1000
def test_query_max_results(max_res):
    with allure.step("send a request"):
        response = query(name=NAME, max_res=max_res)
        attach_code(response.status)

    with allure.step("check status code"):
        assert response.status == 200
    with allure.step("check there are no more results than max_results"):
        assert len(response.entries) <= int(max_res)


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query method")
@allure.title("Check unacceptable values for max_results")
@pytest.mark.parametrize("max_res", [str(sys.maxsize), "notaninteger"])
# for performance reasons, arxiv's maximum number of results
# returned from a single call (max_results) is limited to 30000,
# and they frown upon calls of over 1000
def test_query_max_results(max_res):
    with allure.step("send a request"):
        response = query(name=NAME, max_res=max_res)
        attach_code(response.status)

    with allure.step("check status code"):
        assert response.status == 400


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query method")
@allure.title("The start parameter should change the retrieved entry")
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
@allure.feature("query method")
@allure.title("Check unacceptable values for the start parameter")
@pytest.mark.parametrize("start", ["-1", "notaninteger"])
def test_query_start(start):
    with allure.step("send the request"):
        response = query(name=NAME, start=start, max_res="1")
        attach_code(response.status)

    with allure.step("check status code"):
        assert response.status == 400


@allure.tag("API")
@allure.severity(severity_level=Severity.NORMAL)
@allure.label("owner", 'lankinma')
@allure.feature("query method")
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
@allure.feature("query method")
@allure.title("The id_list parameter should work with query by name")
def test_id_list_with_name():
    with allure.step("send the request"):
        response = query(name=BAD_NAME, id=ID)

    with allure.step("check status code"):
        assert response.status == 200
    with allure.step("check that response is empty"):
        assert len(response.entries) == 0
