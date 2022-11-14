from plone.restapi.interfaces import IExpandableElement
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service

import json


class KitsearchGet(Service):
    def reply(self):
        data = json_body(self.request)

        if not data:
            return {}

        # TODO Get items from elasticsearch. This is an example response:
        from collective.elastic.plone.api.services.kitsearch.response_example import (
            elasticsearchresponse_example,
        )

        elasticsearchresponse = json.loads(elasticsearchresponse_example)

        return elasticsearchresponse
