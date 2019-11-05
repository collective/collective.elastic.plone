# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from Products.CMFCore.interfaces import IIndexQueueProcessor
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class ICollectiveEsPloneLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IElasticSearchIndexQueueProcessor(IIndexQueueProcessor):
    """An index queue processor for elasticsearch."""
