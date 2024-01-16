.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

========================
collective.elastic.plone
========================

OpenSearch or ElasticSearch Integration for Plone content.

It consists of these parts:

- indexer passing content to a separate running `collective.elastic.ingest <https://github.com/collective/collective.elastic.ingest>`_ service.
- catalog index acting as a proxy to Open-/ElasticSearch, integrates with ZCatalog. I.e. use as drop-in replacement for ``SearchableText`` index.
- custom plugins for ``plone.restapi`` to provide structural information for the ingestion service
- REST API endpoint ``@kitsearch`` accepting Open-/ ElasticSearch query returning results with Plone permission check.


.. contents:: Table of Contents

Installation
============

-------------
Preconditions
-------------

You need a working ``collective.elastic.ingest`` (version 2.x) service running.
This implies a running Redis instance and a running Open- xor ElasticSearch instance.

------------
mxdev/mxmake
------------

Add ``collective.elastic.plone[redis,opensearch]>=2.0.0b11`` to your ``requirements.txt`` (alternatively use a ``constraints.txt`` for version pinning).

The extra requirements are needed for the queue server and index server used and may vary, see below.
Alternatively add it to your ``pyproject.toml`` as dependencies (or in case of legacy code to ``setup.[py|cfg]``).

Provide and *source* an environments variable file (i.e. `.env`) in your backend directory before Plone startup with::

    export INDEX_SERVER=localhost:9200
    export INDEX_USE_SSL=1
    export INDEX_OPENSEARCH=1
    export INDEX_LOGIN=admin
    export INDEX_PASSWORD=admin
    export INDEX_NAME=plone
    export CELERY_BROKER=redis://localhost:6379/0


--------
Buildout
--------

Install ``collective.elastic.plone[redis,opensearch]`` by adding it to your buildout.
The extra requirements are needed for the queue server and index server used may vary, see below.
Environment may vary too.
Also, see below.

::

    [buildout]

    # ...

    eggs =
        # ...
        collective.elastic.plone[redis,opensearch]

    environment-vars +=
        INDEX_SERVER=localhost:9200
        INDEX_USE_SSL=1
        INDEX_OPENSEARCH=1
        INDEX_LOGIN=admin
        INDEX_PASSWORD=admin
        INDEX_NAME=plone
        CELERY_BROKER=redis://localhost:6379/0

    [versions]
    collective.elastic.plone = 2.0.0


and run ``bin/buildout``

------------------
Extra requirements
------------------

Depending on the queue server and index server used, the extra requirements vary:

- queue server: ``redis`` or ``rabbitmq``.
- index server: ``opensearch`` or ``elasticsearch``.


-------------
After Startup
-------------

After startup you need to install the addon in Plone via the Addons control panel.
This replaces the SearchableText index with the proxy index and a minimal configuration.
Best is to alter the configuration to the projects needs.

To index all content in the catalog, append ``/@@update-elasticsearch`` to the URL of your Plone site.
This queues all content for indexing in ElasticSearch (but not in the ZCatalog).
Alternatively a reindex catalog (in ZMI under advanced tab) works too.

New or modified content is queued for indexing automatically.


--------------
Volto Frontend
--------------

The proxy index works out of the box in Volto.

However, in Volto a direct (and much faster) search is possible by using the ``@kitsearch`` endpoint, bypassing the catalog.
The endpoint takes a native Open-/ ElasticSearch query and returns the results with Plone permission check.

The Volto add-on `volto-searchkit-block <https://github.com/rohberg/volto-searchkit-block/>`_ (based on `react-searchkit <https://www.npmjs.com/package/react-searchkit>`_) provides a configurable block using this endpoint.

Remark:
For security reasons, in collective.elastic.plone 2.0.0 the ``@kitsearch`` endpoint always overrides any "API URL" and "API index" settings with the configured values from the environment.

Configuration
=============

Global configuration is done via environment variables.

Each catalog proxy-index has its distinct JSON configuration.

-----------
Environment
-----------

Environment variables are:

INDEX_SERVER
    The URL of the ElasticSearch or OpenSearch server.

    Default: localhost:9200

INDEX_NAME
    The name of the index to use at the ElasticSearch or OpenSearch service.

    Default: plone

INDEX_USE_SSL
    Whether to use a secure connection or not.

    Default: 0

INDEX_OPENSEARCH
    Whether to use OpenSearch or ElasticSearch.

    Default: 1

INDEX_LOGIN
    Username for the ElasticSearch 8+ or OpenSearch 2 server.
    For the Plone addon read access is enough.

    Default: admin

INDEX_PASSWORD
    Password of the above user

    Default: admin

CELERY_BROKER
    The broker URL for Celery.
    See `docs.celeryq.dev <https://docs.celeryq.dev/>`_ for details.

    Default: `redis://localhost:6379/0`

-----------
Proxy-index
-----------

Through-the-web, the proxy-index can be configured in the Zope Management Interface (ZMI) under ``portal_catalog``, then click on the ``ElasticSearchProxyIndex`` (i.e. ``SearchableText``).

In the file system it can be configured as any other index in the ``portal_catalog`` tool using a GenericSetup profile and placing a ``catalog.xml`` file in there.
The index configuration looks like so:

.. code-block:: xml

    <index meta_type="ElasticSearchProxyIndex"
            name="SearchableText"
    >
        <querytemplate>
    {
        "query": {
            "multi_match": {
                "query": "{{keys[0]}}",
                "fields": [
                    "title*^1.9",
                    "description*^1.5",
                    "text.data*^1.2",
                    "blocks_plaintext*^1.2"
                    "file__extracted.content*"
                ],
                "analyzer": "{{analyzer}}","operator": "or",
                "fuzziness": "AUTO",
                "prefix_length": 1,
                "type": "most_fields",
                "minimum_should_match": "75%"
            }
        }
    }
        </querytemplate>
    </index>

It uses Jinja2 templates to inject the search term into the query.
Available variables are:

``keys``
    a list of search terms, usually just one.

``language``
    the `current language <https://6.docs.plone.org/plone.api/portal.html#get-current-language>`_ of the portal.

``analyzer``
    the name of the analyzer for the query based on the language.
    This is hardcoded by now. If there is no analyzer for the language, the ``standard`` analyzer is used.

The resulting query needs to be a valid `OpenSearch Query DSL <https://opensearch.org/docs/latest/query-dsl/index/>`_ or `ElasticSearch Query DSL <https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl.html>`_  text.


Source Code
===========

The sources are in a GIT DVCS with its main branches at `github <http://github.com/collective/collective.elastic.plone>`_.
There you can report issue too.

We'd be happy to see many forks and pull-requests to make this addon even better.

Maintainers are `Jens Klein <mailto:jk@kleinundpartner.at>`_, `Peter Holzer <mailto:peter.holzer@agitator.com>`_ and the BlueDynamics Alliance developer team.
We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.
We also offer commercial support if any training, coaching, integration or adaptions are needed.

Releases are done using the Github Release feature and PyPI trusted publishing.
Never use a different release process!
If in doubt ask Jens.


Contributions
=============

Idea and testing: Peter Holzer

Initial concept & code by Jens W. Klein (Github: @jensens)

Contributors:

- Katja Süss (Github: @ksuess)


License
=======

The project is licensed under the GPLv2.
