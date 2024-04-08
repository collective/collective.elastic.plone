from .. import INDEX_NAME
from collective.elastic.ingest.celery import index
try:
    from collective.elastic.ingest.celery import deleteindex
except ImportError:
    deleteindex = None
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
            index.delay(path, 0, INDEX_NAME)
            count += 1
        return f"queued {count}"


class ClearAndUpdateElastisearch(BrowserView):
    def __call__(self):
        # Delete index
        if deleteindex is not None:
            deleteindex.delay(INDEX_NAME)

        # Index content
        cat = api.portal.get_tool("portal_catalog")
        count = 0
        for path in cat._catalog.uids:
            if path.endswith("/portal_catalog"):
                # no idea why it is in the list, ignore
                continue
            index.delay(path, 0, INDEX_NAME)
            count += 1
        return f"Index '{INDEX_NAME}' rebuild."
