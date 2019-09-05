# -*- coding: utf-8 -*-
from App.config import getConfiguration
from elasticsearch import Elasticsearch
from plone import api

import logging
import threading


logger = logging.getLogger(__name__)

INDEX = "plone"

_block_es_queries = threading.local()


def get_es_client():
    config = getConfiguration().product_config.get("elasticsearch", dict())
    addresses = [x for x in config.get("clients", "").split(",") if x.strip()]
    if not addresses:
        addresses.append("127.0.0.1:9200")
    return Elasticsearch(
        addresses,
        use_ssl=config.get("use_ssl", False),
        # here some more params need to be configured.
    )


def index_name():
    portal = api.portal.get()
    return "plone_{0}".format(portal.getId()).lower()


class _QueryBlocker(object):
    @property
    def blocked(self):
        return getattr(_block_es_queries, "blocked", False)

    def block(self):
        return setattr(_block_es_queries, "blocked", True)

    def unblock(self):
        return setattr(_block_es_queries, "blocked", False)


query_blocker = _QueryBlocker()
