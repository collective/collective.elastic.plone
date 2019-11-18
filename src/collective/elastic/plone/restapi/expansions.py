# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from zope.annotation import IAnnotations
from zope.interface import implementer


@implementer(IExpandableElement)
class RidExpansion(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        cat = api.portal.get_tool("portal_catalog")
        path = "/".join(self.context.getPhysicalPath())
        return {"catalog_rid": cat.getrid(path)}


@implementer(IExpandableElement)
class TimestampExpansion(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        annotations = IAnnotations(self.context)
        if annotations is None:
            return {}
        ts = annotations.get("ELASTIC_LAST_INDEXING_QUEUED_TIMESTAMP", 0)
        return {"last_indexing_queued": ts}
