# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("collective.elastic.plone")


def initialize(context):
    from collective.elastic.plone import proxyindex

    context.registerClass(
        proxyindex.ElasticSearchProxyIndex,
        permission="Add Pluggable Index",
        constructors=(proxyindex.manage_addESPIndexForm, proxyindex.manage_addESPIndex),
        icon="www/index.gif",
        visibility=None,
    )
