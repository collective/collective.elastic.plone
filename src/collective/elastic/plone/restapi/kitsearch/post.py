from AccessControl import getSecurityManager
from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from Products.CMFCore.utils import getToolByName
from pprint import pprint
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json
import requests


class Kitsearch(Service):
    """Request to ElasticSearch

    Args:
        query (dict): ElasticSearch query
    """

    def search(self, data):
        elasticsearch_url = data.get("elasticsearch_url", "http://localhost:9200")
        elasticsearch_index = data.get("elasticsearch_index", "plone")
        resp = requests.post(
            f"{elasticsearch_url}/{elasticsearch_index}/_search",
            headers={"Accept": "application/json", "Content-Type": "application/json"},
            json=data.get("elasticsearch_payload", {}),
        )
        return json.loads(resp.text)

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
        if not esquery["elasticsearch_payload"].get("aggs"):
            esquery["elasticsearch_payload"]["aggs"] = {}
        esquery["elasticsearch_payload"]["aggs"]["section_agg"] = {
            "terms": {"field": "section.keyword"}
        }
        print(
            'esquery["elasticsearch_payload"]["aggs"]',
            esquery["elasticsearch_payload"]["aggs"],
        )
        return esquery

    def reply(self):
        data = json_body(self.request)

        if not data:
            return {}

        # # An example response:
        # from collective.elastic.plone.api.services.kitsearch.response_example import (
        #     elasticsearchresponse_example,
        # )

        # elasticsearchresponse = json.loads(elasticsearchresponse_example)

        elasticsearchresponse = self.search(self.esQuery(data))

        return elasticsearchresponse
