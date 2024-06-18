from . import INDEX_NAME
from .interfaces import IElasticSearchIndexQueueProcessor
from collective.elastic.ingest.celery import index
from collective.elastic.ingest.celery import unindex
from kombu.exceptions import OperationalError
from plone import api
from plone.api.exc import CannotGetPortalError
from plone.dexterity.interfaces import IDexterityContent
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.tool import UNKNOWN
from zope.annotation import IAnnotations
from zope.interface import implementer

import logging
import time


logger = logging.getLogger("collective.elastic.plone")


@implementer(IElasticSearchIndexQueueProcessor)
class ElasticSearchIndexQueueProcessor:
    """a queue processor for Open-/ElasticSearch"""

    def _active(self, obj=None):
        try:
            portal_setup = api.portal.get_tool("portal_setup")
        except CannotGetPortalError:
            portal_setup = getToolByName(obj, "portal_setup")

        return (
            portal_setup.getLastVersionForProfile(
                "collective.elastic.plone:default")
            != UNKNOWN
        )

    def index(self, obj, attributes=None):
        if not self._active(obj) or not IDexterityContent.providedBy(obj):
            return
        # get transaction id
        ts = time.time()
        annotations = IAnnotations(obj)
        annotations["ELASTIC_LAST_INDEXING_QUEUED_TIMESTAMP"] = ts
        index.delay("/".join(obj.getPhysicalPath()), ts, INDEX_NAME)

    def reindex(self, obj, attributes=None, update_metadata=1):
        if not self._active(obj):
            logger.error(f"Reindexing of {obj} failed.'")
            return
        try:
            self.index(obj, attributes)
        except OperationalError as e:
            logger.exception(
                f"ElasticSearchIndexQueueProcessor. Reindexing failed: {str(e)}. "
                "Check Open-/ ElasticSearch configuration."
            )

    def unindex(self, obj):
        if not self._active(obj):
            return
        uid = api.content.get_uuid(obj)
        unindex.delay(uid, INDEX_NAME)

    def begin(self):
        pass

    def commit(self, wait=None):
        pass

    def abort(self):
        pass
