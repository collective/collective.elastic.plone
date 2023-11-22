# -*- coding: utf-8 -*-
from collective.elastic.ingest.celery import index
from collective.elastic.ingest.celery import unindex
from collective.elastic.plone.eslib import index_name
from collective.elastic.plone.interfaces import IElasticSearchIndexQueueProcessor
from kombu.exceptions import OperationalError
from plone import api
from plone.dexterity.interfaces import IDexterityContent
from zope.annotation import IAnnotations
from zope.interface import implementer
from Products.GenericSetup.tool import UNKNOWN

import logging
import time


logger = logging.getLogger("collective.elastic.index")


@implementer(IElasticSearchIndexQueueProcessor)
class ElasticSearchIndexQueueProcessor(object):
    """a queue processor for Open-/ElasticSearch"""

    def _active(self):
        portal_setup = api.portal.get_tool("portal_setup")
        return portal_setup.getLastVersionForProfile("collective-elastic-plone") != UNKNOWN

    def index(self, obj, attributes=None):
        if not self._active() or not IDexterityContent.providedBy(obj):
            return
        # get transaction id
        ts = time.time()
        annotations = IAnnotations(obj)
        annotations["ELASTIC_LAST_INDEXING_QUEUED_TIMESTAMP"] = ts
        index.delay("/".join(obj.getPhysicalPath()), ts, index_name())

    def reindex(self, obj, attributes=None, update_metadata=1):
        if not self._active():
            return
        try:
            self.index(obj, attributes)
        except OperationalError as e:
            logger.exception(
                f"ElasticSearchIndexQueueProcessor. Reindexing failed: {str(e)}. "
                "Check Open-/ ElasticSearch configuration."
            )

    def unindex(self, obj):
        if not self._active():
            return
        uid = api.content.get_uuid(obj)
        unindex.delay(uid, index_name())

    def begin(self):
        pass

    def commit(self, wait=None):
        pass

    def abort(self):
        pass
