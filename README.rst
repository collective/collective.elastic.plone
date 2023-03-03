.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

========================
collective.elastic.plone
========================

ElasticSearch Integration for Plone content

- indexer passing content to a separate running `collective.elastic.ingest <https://github.com/collective/collective.elastic.ingest>`_ service.
- index acting as a proxy to ElasticSearch, integrates with ZCatalog
- custom plugins for `plone.restapi` to provide structural information for the ingestions service
- REST api endpoint @kitsearch accepting Elasticsearch query returning results with Plone permission check.


Installation
------------

**mxdev**

Add `collective.elastic.plone` to your `requirements.txt`.
Provide an environments variable file `.env` in your backend directory with::

    export CELERY_BROKER=redis://localhost:6379/0
    export ELASTICSEARCH_INDEX={{elasticsearchindex}}
    export ELASTICSEARCH_QUERY_SERVER={{elasticsearch_address}}


**buildout**

Install `collective.elastic.plone` by adding it to your buildout::

    [buildout]

    ...

    eggs =
        ...
        collective.elastic.plone

    environment-vars +=
        CELERY_BROKER redis://localhost:6379/0
        ELASTICSEARCH_INDEX plone
        ELASTICSEARCH_QUERY_SERVER http://localhost:9200
        ELASTICSEARCH_QUERY_USE_SSL 0



and then running ``bin/buildout``


Source Code
-----------

The sources are in a GIT DVCS with its main branches at `github <http://github.com/collective/collective.elastic.index>`_.
There you can report issue too.

We'd be happy to see many forks and pull-requests to make this addon even better.

Maintainers are `Jens Klein <mailto:jk@kleinundpartner.at>`_, `Peter Holzer <mailto:peter.holzer@agitator.com>`_ and the BlueDynamics Alliance developer team.
We appreciate any contribution and if a release is needed to be done on pypi, please just contact one of us.
We also offer commercial support if any training, coaching, integration or adaptions are needed.


Contributions
-------------

Initial implementation was made possible by `Evangelisch-reformierte Landeskirche des Kantons Zürich <http://zhref.ch/>`_.

Idea and testing: Peter Holzer

Concept & code by Jens W. Klein

Authors:

- Katja Süss (Github: @ksuess)


License
-------

The project is licensed under the GPLv2.
