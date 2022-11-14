from plone.restapi.deserializer import json_body
from plone.restapi.services import Service

import json
import requests


def search(data):
    elasticsearch_url = data.get("elasticsearch_url", "http://localhost:9200")
    elasticsearch_index = data.get("elasticsearch_index", "plone")
    resp = requests.post(
        f"{elasticsearch_url}/{elasticsearch_index}/_search",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json=data.get("elasticsearch_payload", {}),
    )
    return json.loads(resp.text)


class KitsearchGet(Service):
    def reply(self):
        data = json_body(self.request)

        if not data:
            return {}

        # # An example response:
        # from collective.elastic.plone.api.services.kitsearch.response_example import (
        #     elasticsearchresponse_example,
        # )

        # elasticsearchresponse = json.loads(elasticsearchresponse_example)

        elasticsearchresponse = search(data)

        return elasticsearchresponse
