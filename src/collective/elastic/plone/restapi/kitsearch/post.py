from ... import INDEX_NAME
from AccessControl import getSecurityManager
from collective.elastic.ingest import OPENSEARCH
from collective.elastic.ingest.client import get_client
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName

import deepmerge
import logging


if OPENSEARCH:
    from opensearchpy.exceptions import NotFoundError
    from opensearchpy.exceptions import RequestError
    from opensearchpy.exceptions import TransportError
else:
    from elasticsearch.exceptions import NotFoundError
    from elasticsearch.exceptions import RequestError
    from elasticsearch.exceptions import TransportError


logger = logging.getLogger(__name__)


class Kitsearch(Service):
    """Request to Open-/ElasticSearch

    Args:
        query (dict): elasticsearch_url, INDEX_NAME, elasticsearch_payload (query)
    """

    def reply(self):
        data = json_body(self.request)

        if not data:
            return {}

        return self.search(self._extend_es_query(data))

    def search(self, data):
        """Fetch with Python elasticsearch module."""
        # for security reasons we do not allow to pass the index name and the elasticsearch_url
        # in the request body. Instead we use the values from the config.

        query_body = data.get("elasticsearch_payload", {})

        search_kwargs = dict(
            index=INDEX_NAME,
            body=query_body,
        )
        if not query_body.get("size", None):
            search_kwargs["size"] = 10
        indexer_client = get_client()
        result = indexer_client.search(**search_kwargs)
        # result is of type ObjectApiResponse
        return dict(result)

    def _extend_es_query(self, esquery):
        """Extend query with roles, user and groups."""
        if getSecurityManager().checkPermission("Manage portal", self.context):
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
