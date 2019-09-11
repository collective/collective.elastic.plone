# -*- coding: utf-8 -*-
from App.config import getConfiguration
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import zope


class CollectiveEsPloneLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        import collective.es.plone

        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.es.plone)
        zope.installProduct(app, "collective.es.plone")

    def setUpPloneSite(self, portal):
        getConfiguration().product_config = {"addresses": "localhost:9200"}
        applyProfile(portal, "collective.es.plone:default")


COLLECTIVE_ES_PLONE_FIXTURE = CollectiveEsPloneLayer()


COLLECTIVE_ES_PLONE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ES_PLONE_FIXTURE,),
    name="CollectiveEsPloneLayer:IntegrationTesting",
)


COLLECTIVE_ES_PLONE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ES_PLONE_FIXTURE,),
    name="CollectiveEsPloneLayer:FunctionalTesting",
)
