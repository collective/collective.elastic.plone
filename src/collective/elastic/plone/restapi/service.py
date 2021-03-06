# -*- coding: utf-8 -*-
from plone.restapi.services import Service as BaseService
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


class Service(BaseService):
    def render(self):
        self.check_permission()
        content = self.reply()
        self.request.response.setHeader("Content-Type", self.content_type)
        return json.dumps(content, indent=2, sort_keys=True, separators=(", ", ": "))


@implementer(IPublishTraverse)
class TraversingService(Service):
    def __init__(self, context, request):
        super(TraversingService, self).__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@registry as parameters
        self.params.append(name)
        return self
