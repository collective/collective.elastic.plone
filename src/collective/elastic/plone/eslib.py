from . import INDEX_NAME
from collective.elastic.ingest.client import get_client

import logging


logger = logging.getLogger(__name__)


def get_query_client(elasticsearch_server_baseurl=None):
    """return elasticsearch client for ingest"""
    logger.warn(
        ".eslib.get_query_client is deprecated, "
        "use collective.elastic.ingest.client.client.get_client instead"
    )
    return get_client(elasticsearch_server_baseurl)


def index_name():
    logger.warn(".eslib.index_name is deprecated, use global .INDEX_NAME instead")
    return INDEX_NAME
