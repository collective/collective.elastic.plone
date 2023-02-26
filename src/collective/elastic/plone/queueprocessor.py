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

import logging
import time


logger = logging.getLogger("collective.elastic.index")


@implementer(IElasticSearchIndexQueueProcessor)
class ElasticSearchIndexQueueProcessor(object):
    """a queue processor for ElasticSearch"""

    def index(self, obj, attributes=None):
        if not IDexterityContent.providedBy(obj):
            return
        # get transaction id
        ts = time.time()
        annotations = IAnnotations(obj)
        annotations["ELASTIC_LAST_INDEXING_QUEUED_TIMESTAMP"] = ts
        index.delay("/".join(obj.getPhysicalPath()), ts, index_name())

    def reindex(self, obj, attributes=None, update_metadata=1):
        try:
            self.index(obj, attributes)
        except OperationalError as e:
            logger.exception(
                f"ElasticSearchIndexQueueProcessor. Reindexing failed: {str(e)}. Check ElasticSearch configuration."
            )

    def unindex(self, obj):
        uid = api.content.get_uuid(obj)
        unindex.delay(uid, index_name())

    def begin(self):
        pass

    def commit(self, wait=None):
        pass

    def abort(self):
        pass
