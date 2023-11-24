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

You need a working ``collective.elastic.ingest`` service running.
This implies a running Redis instance and a running Open- xor ElasticSearch instance.

------------
mxdev/mxmake
------------

Add ``collective.elastic.plone[redis,opensearch]`` to your ``requirements.txt``.
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

Install `collective.elastic.plone` by adding it to your buildout::

    [buildout]

    # ...

    eggs =
        # ...
        collective.elastic.plone

    environment-vars +=
        INDEX_SERVER=localhost:9200
        INDEX_USE_SSL=1
        INDEX_OPENSEARCH=1
        INDEX_LOGIN=admin
        INDEX_PASSWORD=admin
        INDEX_NAME=plone
        CELERY_BROKER=redis://localhost:6379/0


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
To index all content a manual re-index of the catalog is needed.

--------------
Volto Frontend
--------------

The proxy index works out of the box in Volto.

However, in Volto a direct (and much faster) search is possible by using the ``@kitsearch`` endpoint, bypassing the catalog.
The endpoint takes a native Open-/ ElasticSearch query and returns the results with Plone permission check.

The Volto add-on `volto-searchkit-block <https://github.com/rohberg/volto-searchkit-block/>`_ provides a configurable block using this endpoint.


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

Trough-the-web the proxy-index can be configured in the Zope Management Interface (ZMI) under ``portal_catalog``, then click on the ``ElasticSearchProxyIndex`` (i.e. ``SearchableText``).

In the file system it can be configured as any other index in the ``portal_catalog`` tool using a GenericSetup profile and placing a ``catalog.xml`` file in there.
The index configuration looks like so:

```xml
  <index meta_type="ElasticSearchProxyIndex"
         name="SearchableText"
  >
    <querytemplate>
{
    "query":{
        "bool":{
            "should":[
                    {
                        "query_string":{
                            "query":"{{keys[0].decode('utf8')}}",
                            "fields":[
                                "title^1.2",
                                "id",
                                "description^1.1",
                                "subjects^2"
                                ]
                        }
                    },
                    {
                        "nested":{
                            "path":"text__extracted",
                            "query":{
                                "query_string":{
                                    "query":"{{keys[0].decode('utf8')}}",
                                    "fields":["text__extracted.content"]
                                }
                            }
                        }
                    },
                    {
                        "nested":{
                            "path":"file__extracted",
                            "query":{
                                "query_string":{
                                    "query":"{{keys[0].decode('utf8')}}",
                                    "fields":["file__extracted.content"]
                                }
                            }
                        }
                    },
                    {
                        "nested":{
                            "path":"image__extracted",
                            "query":{
                                "query_string":{
                                    "query":"{{keys[0].decode('utf8')}}",
                                    "fields":["image__extracted.content"]
                            }
                        }
                    }
                }
            ]
        }
    }
}
    </querytemplate>
```

It uses Jinja2 templating to inject the search term into the query.
The variable ``keys`` is a list of search terms, usually just one.
The resulting query is a standard ElasticSearch query.


Source Code
===========

The sources are in a GIT DVCS with its main branches at `github <http://github.com/collective/collective.elastic.plone>`_.
There you can report issue too.

We'd be happy to see many forks and pull-requests to make this addon even better.

Maintainers are `Jens Klein <mailto:jk@kleinundpartner.at>`_, `Peter Holzer <mailto:peter.holzer@agitator.com>`_ and the BlueDynamics Alliance developer team.
We appreciate any contribution and if a release is needed to be done on PyPI, please just contact one of us.
We also offer commercial support if any training, coaching, integration or adaptions are needed.


Contributions
=============

Idea and testing: Peter Holzer

Initial concept & code by Jens W. Klein

Contributors:

- Katja Süss (Github: @ksuess)


License
=======

The project is licensed under the GPLv2.
