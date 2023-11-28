Changelog
=========


2.0.0a1 (unreleased)
--------------------

- Do not expect Volto to be installed/available.
  Works now in plain Classic UI again. [jensens]
- Fix: Do not index if indexer is not installed. [jensens]
- Package: use mxmake/mxdev and go Plone 6 only [jensens]
- Package: use pyproject.toml, drop setup.*, pep420 [jensens]
- Code-style: black, isort, zpretty, pyupgrade [jensens]
- Remove Plone 5 bbb imports. [jensens]
- Minor refactoring of kitsearch to be more readable, introduce deepmerge package [jensens]
- Rename env var ELASTICSEARCH_INDEX to INDEX_NAME.
  This way we are harmonized with collective.elastic.ingest, which uses the INDEX_ prefix in 2.x. [jensens]
- Refactoring: Retire eslib, use collective.elastic.ingest.client.get_client and INDEX_NAME as global instead. [jensens]
- Test: Refactor to use pytest [jensens]
- Feature: @cesp endpoint gets language support [jensens]
- Fix tests and mock Elasticsearch client [jensens]
- Feature: Add current language code and mapped analyzer to query template [jensens]
- Feature: Reduce default query-template to a simple query and use analyzer [jensens]
- Security @kitsearch endpoint: We do not allow to pass the index name and the elasticsearch_url in the request body.
  Instead we use the values from the config. [jensens]


1.1.4 (2023-08-17)
------------------

- Get elastic client getter from collective.elastic.ingest. [ksuess]
- Refactor to one single IExpandableElement adapter. [ksuess]
- Add IBlockSearchableText adapter for accordion block. [ksuess]
- Add IBlockSearchableText adapter for teaser block. [ksuess]


1.1.3 (2023-04-22)
------------------

- Step back from ElasticSearch scroll API for deep pagination.


1.1.2 (2023-03-04)
------------------

-  Enhance response of @kitsearch on unavailable ElasticSearch or not found index [ksuess]


1.1.1 (2023-03-03)
------------------

- Nothing changed yet.


1.1 (2023-03-03)
----------------

- Search REST API service @kitsearch for ElasticSearch querying with Plone security check. [ksuess]


1.0 (2022-11-08)
----------------

- Initial release.
  [jensens]
