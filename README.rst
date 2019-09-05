.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

===================
collective.es.plone
===================

ElasticSearch Integration for Plone content

- indexer passing content to an `collective.es.ingestion` service.
- index acting as a proxy to ElasticSearch, integrates with ZCatalog
- custom plugins for `plone.restapi` to provide strcutural information for the igestions service

Installation
------------

Install collective.es.plone by adding it to your buildout::

    [buildout]

    ...

    eggs =
        ...
        collective.es.plone

    zope-conf-additional =
        ...
        <product-config elasticsearch>
            addresses localhost:9200
            use-ssl false
        <product-config>


and then running ``bin/buildout``


Source Code
-----------

The sources are in a GIT DVCS with its main branches at `github <http://github.com/collective/collective.es.index>`_.
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

- no others so far


License
-------

The project is licensed under the GPLv2.
