from AccessControl import getSecurityManager
from collective.elastic.plone.eslib import get_query_client
from elasticsearch.exceptions import RequestError
from elasticsearch.exceptions import TransportError
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from pprint import pprint

import json
import requests
import logging


logger = logging.getLogger(__name__)


class Kitsearch(Service):
    """Request to ElasticSearch

    Args:
        query (dict): elasticsearch_url, elasticsearch_index, elasticsearch_payload (query)
    """

    def searchSimple(self, data):
        """Simple fetch with Python requests module."""

        elasticsearch_url = data.get("elasticsearch_url", "http://localhost:9200")
        elasticsearch_index = data.get("elasticsearch_index", "plone")
        resp = requests.post(
            f"{elasticsearch_url}/{elasticsearch_index}/_search",
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            json=data.get("elasticsearch_payload", {}),
        )
        resp.raise_for_status()
        return json.loads(resp.text)

    def search(self, data):
        """Fetch with Python elasticsearch module."""

        elasticsearch_url = data.get("elasticsearch_url", "http://localhost:9200")
        elasticsearch_index = data.get("elasticsearch_index", "plone")
        query_body = data.get("elasticsearch_payload", {})

        es_kwargs = dict(
            index=elasticsearch_index,
            body=query_body,
            scroll="1m",
            # _source_includes=["rid"],
        )
        if not query_body.get("size", None):
            es_kwargs["size"] = 10
        es = get_query_client(elasticsearch_url)
        try:
            result = es.search(**es_kwargs)
        except RequestError as e:
            logger.exception(f"Query failed: {str(e)}")
            logger.exception(pprint(query_body))
            return None, str(e)
        except TransportError as e:
            logger.exception(f"ElasticSearch failed {str(e)}")
            return None, str(e)
        # result is of type ObjectApiResponse
        return dict(result), ""

    def has_permission_to_query_all(self):
        sm = getSecurityManager()
        return sm.checkPermission("Manage portal", self.context)

    def esQuery(self, data):
        """Extend query with roles, user and groups"""
        esquery = data
        if self.has_permission_to_query_all():
            pass
        else:
            mtool = getToolByName(self.context, "portal_membership")
            if bool(mtool.isAnonymousUser()):
                arau = ["Anonymous"]
            else:
                user = mtool.getAuthenticatedMember()
                username = user.getId()
                roles = api.user.get_roles(username=username)
                groups = api.group.get_groups(username=username)
                arau = roles
                arau.append(f"user:{username}")
                for grp in groups:
                    arau.append(f"user:{grp.id}")
                arau.append("Anonymous")

            # Enrich original query with "allowedRolesAndUsers"
            if not esquery["elasticsearch_payload"].get("post_filter"):
                esquery["elasticsearch_payload"] = {"bool": {"must": []}}
            if not esquery["elasticsearch_payload"]["post_filter"].get("bool"):
                esquery["elasticsearch_payload"]["post_filter"] = {"bool": {"must": []}}
            if not esquery["elasticsearch_payload"]["post_filter"]["bool"].get("must"):
                esquery["elasticsearch_payload"]["post_filter"]["bool"] = {"must": []}
            esquery["elasticsearch_payload"]["post_filter"]["bool"]["must"].append(
                {"terms": {"allowedRolesAndUsers.keyword": arau}}
            )
        # Enrich query with aggregation info on sections
        # And apply filter to aggregation per section
        if not esquery["elasticsearch_payload"].get("aggs"):
            esquery["elasticsearch_payload"]["aggs"] = {}
        post_filter_filter = (
            esquery["elasticsearch_payload"]
            .get("post_filter", {})
            .get("bool", {})
            .get("filter", [])
        )
        post_filter_must = (
            esquery["elasticsearch_payload"]
            .get("post_filter", {})
            .get("bool", {})
            .get("must", [])
        )
        post_filter_must_without_section = [
            flt for flt in post_filter_must if not "section" in flt["terms"].keys()
        ]
        esquery["elasticsearch_payload"]["aggs"]["section_agg"] = {
            "aggs": {
                "section_foodidoo": {"terms": {"field": "section.keyword", "size": 500}}
            },
            # With filter it's not easy as
            # "terms": {"field": "section.keyword"},
            "filter": {
                "bool": {
                    "filter": post_filter_filter,
                    "must": post_filter_must_without_section,
                }
            },
        }
        return esquery

    def reply(self):
        data = json_body(self.request)

        if not data:
            return {}

        elasticsearchresponse = self.searchSimple(self.esQuery(data))
        return elasticsearchresponse
