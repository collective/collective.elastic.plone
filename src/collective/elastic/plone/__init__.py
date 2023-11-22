"""Init and utils."""
from zope.i18nmessageid import MessageFactory

import os


_ = MessageFactory("collective.elastic.plone")

INDEX_NAME = os.environ.get("INDEX_NAME", "plone")


def initialize(context):
    from collective.elastic.plone import proxyindex

    context.registerClass(
        proxyindex.ElasticSearchProxyIndex,
        permission="Add Pluggable Index",
        constructors=(proxyindex.manage_addESPIndexForm, proxyindex.manage_addESPIndex),
        icon="www/index.gif",
        visibility=None,
    )
