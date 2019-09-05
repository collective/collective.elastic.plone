# -*- coding: utf-8 -*-
"""Init and utils."""
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("collective.es.plone")


def initialize(context):
    from collective.es.plone import proxyindex

    context.registerClass(
        proxyindex.ElasticSearchProxyIndex,
        permission="Add Pluggable Index",
        constructors=(proxyindex.manage_addESPIndexForm, proxyindex.manage_addESPIndex),
        icon="www/index.gif",
        visibility=None,
    )
