from io import BytesIO

import allure
from allure_commons.types import Severity
import requests
from lxml import etree

from tests.conftest import QUERY_XSD


@allure.tag("API")
@allure.severity(severity_level=Severity.CRITICAL)
# @allure.label("owner", 'lankinma')
@allure.feature("search query")
@allure.title("Ensure search query response is well-formed")
def test_search_query():
    schema_doc = etree.parse(QUERY_XSD)
    schema = etree.XMLSchema(schema_doc)

    response = requests.get(url="http://export.arxiv.org/api/query?search_query=all:electron")
    xml_doc = etree.parse(BytesIO(bytes(response.text, 'utf-8')))

    assert response.status_code == 200
    assert schema.validate(xml_doc)
