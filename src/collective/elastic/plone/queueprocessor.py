# -*- coding: utf-8 -*-
from collective.elastic.ingest.celery import index
from collective.elastic.ingest.celery import unindex
from collective.elastic.plone.eslib import index_name
from collective.elastic.plone.interfaces import IElasticSearchIndexQueueProcessor
from persistent.timestamp import TimeStamp
from plone import api
from zope.interface import implementer

import logging


logger = logging.getLogger("collective.elastic.index")


@implementer(IElasticSearchIndexQueueProcessor)
class ElasticSearchIndexQueueProcessor(object):
    """ a queue processor for ElasticSearch"""

    def index(self, obj, attributes=None):
        # get transaction id
        ts = TimeStamp(obj._p_serial)
        index.delay("/".join(obj.getPhysicalPath()), ts.timeTime(), index_name())

    def reindex(self, obj, attributes=None, update_metadata=1):
        self.index(obj, attributes)

    def unindex(self, obj):
        uid = api.content.get_uuid(obj)
        unindex.delay(uid, index_name())

    def begin(self):
        pass

    def commit(self, wait=None):
        pass

    def abort(self):
        pass
