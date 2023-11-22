# -*- coding: utf-8 -*-
from collective.elastic.ingest.elastic import get_ingest_client

import logging
import os


logger = logging.getLogger(__name__)


def get_query_client(elasticsearch_server_baseurl=None):
    """return elasticsearch client for ingest"""
    return get_ingest_client(elasticsearch_server_baseurl=elasticsearch_server_baseurl)


def index_name():
    return os.environ.get("ELASTICSEARCH_INDEX", "plone")
