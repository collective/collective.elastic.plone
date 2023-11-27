from pytest_plone import fixtures_factory
from collective.elastic.plone.testing import COLLECTIVE_ES_PLONE_FUNCTIONAL_TESTING
from collective.elastic.plone.testing import COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

pytest_plugins = ["pytest_plone"]


globals().update(
    fixtures_factory(
        (
            (COLLECTIVE_ES_PLONE_FUNCTIONAL_TESTING, "functional"),
            (COLLECTIVE_ES_PLONE_INTEGRATION_TESTING, "integration"),
        )
    )
)
