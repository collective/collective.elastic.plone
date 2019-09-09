# -*- coding: utf-8 -*-
from collective.es.plone.interfaces import IElasticSearchIndexQueueProcessor
from collective.es.ingestion.celery import index
from collective.es.ingestion.celery import unindex
from plone import api
from zope.interface import implementer
from persistent.timestamp import TimeStamp

import logging


logger = logging.getLogger('collective.es.index')


@implementer(IElasticSearchIndexQueueProcessor)
class ElasticSearchIndexQueueProcessor(object):
    """ a queue processor for ElasticSearch"""

    def index(self, obj, attributes=None):
        # get transaction id
        ts = TimeStamp(obj._p_serial)
        index.delay('/'.join(obj.getPhysicalPath()), ts.timeTime())

    def reindex(self, obj, attributes=None, update_metadata=1):
        self.index(obj, attributes)

    def unindex(self, obj):
        uid = api.content.get_uuid(obj)
        unindex.delay(uid)

    def begin(self):
        pass

    def commit(self, wait=None):
        pass

    def abort(self):
        pass
