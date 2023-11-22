from AccessControl import getSecurityManager
from collective.elastic.plone.eslib import get_query_client
from elasticsearch.exceptions import NotFoundError
from elasticsearch.exceptions import RequestError
from elasticsearch.exceptions import TransportError
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName

import deepmerge
import json
import logging
import requests


logger = logging.getLogger(__name__)


class Kitsearch(Service):
    """Request to Open-/ElasticSearch

    Args:
        query (dict): elasticsearch_url, INDEX_NAME, elasticsearch_payload (query)
    """

    # def searchSimple(self, data):
    #     """Simple fetch with Python requests module."""
    #     # dead code?
    #     elasticsearch_url = data.get("elasticsearch_url", "http://localhost:9200")
    #     INDEX_NAME = data.get("INDEX_NAME", "plone")
    #     resp = requests.post(
    #         f"{elasticsearch_url}/{INDEX_NAME}/_search",
    #         headers={
    #             "Accept": "application/json",
    #             "Content-Type": "application/json",
    #         },
    #         json=data.get("elasticsearch_payload", {}),
    #     )
    #     return json.loads(resp.text)

    def reply(self):
        data = json_body(self.request)

        if not data:
            return {}

        return self.search(self._extend_es_query(data))

    def search(self, data):
        """Fetch with Python elasticsearch module."""

        elasticsearch_url = data.get("elasticsearch_url", "http://localhost:9200")
        INDEX_NAME = data.get("INDEX_NAME", "plone")
        query_body = data.get("elasticsearch_payload", {})

        es_kwargs = dict(
            index=INDEX_NAME,
            body=query_body,
            # _source_includes=["rid"],
        )
        if not query_body.get("size", None):
            es_kwargs["size"] = 10
        es = get_query_client(elasticsearch_url)
        try:
            result = es.search(**es_kwargs)
        except RequestError as e:
            self.request.response.setStatus(500)
            return dict(error=dict(message=e.message))
        except TransportError as e:
            self.request.response.setStatus(503)
            return dict(error=dict(message=e.message))
        except NotFoundError as e:
            self.request.response.setStatus(404)
            return dict(error=dict(message=e.body["error"]["reason"]))
        except Exception as e:
            self.request.response.setStatus(500)
            return dict(error=dict(message=e.message))
        # result is of type ObjectApiResponse
        return dict(result)

    def _extend_es_query(self, esquery):
        """Extend query with roles, user and groups."""
        if getSecurityManager.sm.checkPermission("Manage portal", self.context):
            # god-mode: query without allowedRolesAndUsers
            return esquery
        mtool = getToolByName(self.context, "portal_membership")
        arau = ["Anonymous"]  # always, if if logged in
        if not mtool.isAnonymousUser():
            user = mtool.getAuthenticatedMember()
            username = user.getId()
            arau.append(f"user:{username}")
            arau += user.getRoles()
            for group in api.group.get_groups(user=user):
                arau.append(f"user:{group.id}")

        # Enrich original query post_filter with "allowedRolesAndUsers".
        # base filter is
        arau_filter = {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "allowedRolesAndUsers.keyword": arau,
                        },
                    }
                ],
            },
        }

        # add as postfilter to main query
        espl = esquery["elasticsearch_payload"]
        espl = deepmerge.always_merger.merge(espl, {"post_filter": arau_filter})

        # enrich each aggregation (aggs) this filter.
        arau_agg_filter = {"filter": arau_filter}
        for agg in espl["aggs"].keys():
            espl["aggs"][agg] = deepmerge.always_merger.merge(
                espl["aggs"][agg], arau_agg_filter
            )

        return esquery
