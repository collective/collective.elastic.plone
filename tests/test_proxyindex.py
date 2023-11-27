"""Setup tests for this package."""
from collective.elastic.plone.testing import COLLECTIVE_ES_PLONE_INTEGRATION_TESTING
from unittest.mock import patch

import os
import unittest


TEST_TEMPLATE_SIMPLE = """\
{
    "foo": "{{bar}}"
}
"""

TEST_TEMPLATE_MATCH_ALL = """\
{
    "query": {
        "match_all": {}
    }
}
"""

TEST_TEMPLATE_FULLTEXT = """\
{
    "query":{
        "query_string":{
            "query":"{{keys[0].replace('"', '')}}",
            "fields":[
                "title^1.2",
                "description^1.1",
                "subjects^2",
                "searchterms^3",
                "extracted_text",
                "extracted_file"
            ]
        }
    }
}
"""


class TestESProxyIndexBasics(unittest.TestCase):
    """Test that proxy index works properly."""

    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for following tests."""
        self.catalog = self.layer["portal"]["portal_catalog"]
        # install index
        from collective.elastic.plone.proxyindex import ElasticSearchProxyIndex

        espi = ElasticSearchProxyIndex(
            "espi", extra={"query_template": TEST_TEMPLATE_SIMPLE}, caller=self.catalog
        )
        self.catalog.addIndex("espi", espi)
        os.environ["INDEX_SERVER"] = "http://localhost:9200"

    def test_index_installed(self):
        """Test if proxy index is installed."""
        self.assertIn("espi", self.catalog.indexes())

    def test_template(self):
        idx = self.catalog._catalog.indexes["espi"]
        result = idx._apply_template({"bar": "baz"})
        self.assertEqual(result["foo"], "baz")


class TestESProxyIndexAllQuery(unittest.TestCase):
    """Test that proxy index works properly."""

    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for following tests."""
        self.catalog = self.layer["portal"]["portal_catalog"]
        # install index
        from collective.elastic.plone.proxyindex import ElasticSearchProxyIndex

        espi = ElasticSearchProxyIndex(
            "espi",
            extra={"query_template": TEST_TEMPLATE_MATCH_ALL},
            caller=self.catalog,
        )
        self.catalog.addIndex("espi", espi)

    def test_query(self):
        idx = self.catalog._catalog.indexes["espi"]
        with patch("elasticsearch.Elasticsearch.search") as mock:
            mock.return_value = {
                "hits": {
                    "hits": [
                        {
                            "_id": "100",
                            "_score": 1.0,
                            "_source": {
                                "rid": -1,
                            },
                        },
                        {
                            "_id": "101",
                            "_score": 0.9,
                            "_source": {
                                "rid": -2,
                            },
                        },
                    ],
                    "total": {
                        "value": 2,
                    },
                },
            }
            result = idx._apply_index({"espi": {"query": "foo"}})

        self.assertGreater(len(result[0]), 1)


class TestESProxyIndexFulltext(unittest.TestCase):
    """Test that proxy index works properly."""

    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for following tests."""
        self.catalog = self.layer["portal"]["portal_catalog"]
        # install index
        from collective.elastic.plone.proxyindex import ElasticSearchProxyIndex

        espi = ElasticSearchProxyIndex(
            "espi",
            extra={"query_template": TEST_TEMPLATE_FULLTEXT},
            caller=self.catalog,
        )
        self.catalog.addIndex("espi", espi)

    def test_query_empty_result(self):
        idx = self.catalog._catalog.indexes["espi"]
        with patch("elasticsearch.Elasticsearch.search") as mock:
            mock.return_value = {
                "hits": {
                    "hits": [
                    ],
                    "total": {
                        "value": 0,
                    },
                },
            }
            result = idx._apply_index({"espi": {"query": "foo"}})
        self.assertEqual(len(result[0]), 0)
