# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class Kitsearch(object):
    def __init__(self, context, request):
        self.context = context.aq_explicit
        self.request = request

    def __call__(self, expand=False, data=None):
        result = {
            "kitsearch": {
                "@id": "{}/@kitsearch".format(
                    self.context.absolute_url(),
                ),
            },
        }

        if not expand:
            return result

        if not data:
            return result

        # TODO get items from elasticsearch
        from collective.elastic.plone.api.services.kitsearch.response_example import (
            elasticsearchresponse,
        )

        result["kitsearch"]["elasticsearchresponse"] = elasticsearchresponse
        return result


class KitsearchGet(Service):
    def reply(self):
        data = json_body(self.request)
        service_factory = Kitsearch(self.context, self.request)
        return service_factory(expand=True, data=data)["kitsearch"]
