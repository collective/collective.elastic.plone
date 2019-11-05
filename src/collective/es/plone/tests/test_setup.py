# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.elastic.plone.testing import COLLECTIVE_ES_PLONE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.CMFPlone.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that collective.elastic.plone is properly installed."""

    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if collective.elastic.plone is installed."""
        self.assertTrue(self.installer.isProductInstalled("collective.elastic.plone"))

    def test_browserlayer(self):
        """Test that ICollectiveEsPloneLayer is registered."""
        from collective.elastic.plone.interfaces import ICollectiveEsPloneLayer
        from plone.browserlayer import utils

        self.assertIn(ICollectiveEsPloneLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstallProducts(["collective.elastic.plone"])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if collective.elastic.plone is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled("collective.elastic.plone"))

    def test_browserlayer_removed(self):
        """Test that ICollectiveEsPloneLayer is removed."""
        from collective.elastic.plone.interfaces import ICollectiveEsPloneLayer
        from plone.browserlayer import utils

        self.assertNotIn(ICollectiveEsPloneLayer, utils.registered_layers())
