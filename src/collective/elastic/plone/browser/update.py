# -*- coding: utf-8 -*-
from collective.elastic.ingest.celery import index
from collective.elastic.plone.eslib import index_name
from plone import api
from Products.Five.browser import BrowserView


class UpdateElastisearch(BrowserView):
    def __call__(self):
        cat = api.portal.get_tool("portal_catalog")
        count = 0
        for path in cat._catalog.uids:
            if path.endswith("/portal_catalog"):
                # no idea why it is in the list, ignore
                continue
            index.delay(path, 0, index_name())
            count += 1
        return "queued {0}".format(count)
