# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
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
