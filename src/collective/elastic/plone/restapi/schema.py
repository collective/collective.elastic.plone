# -*- coding: utf-8 -*-
from collective.elastic.plone.restapi.service import Service
from plone.behavior.interfaces import IBehavior
from Products.CMFCore.interfaces import ITypeInformation
from zope.component import getAllUtilitiesRegisteredFor
from zope.schema import getFieldsInOrder


def dottedname(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__  # Avoid reporting __builtin__
    else:
        return module + "." + obj.__class__.__name__


def _field(field, name=None):
    """serialize a single field definition for ES
    """
    record = {"field": dottedname(field)}
    if name:
        record["name"] = name
    value_type = getattr(field, "value_type", None)
    if value_type:
        record["value_type"] = _field(value_type)
    return record


class SchemaService(Service):
    def _fields(self, schema):
        return [_field(field, name=name) for name, field in getFieldsInOrder(schema)]

    def reply(self):
        result = {"types": {}, "behaviors": {}}
        for fti in getAllUtilitiesRegisteredFor(ITypeInformation):
            try:
                fields = self._fields(fti.lookupSchema())
            except (AttributeError, ValueError):
                continue
            if fields:
                result["types"][fti.getId()] = fields

        for registration in getAllUtilitiesRegisteredFor(IBehavior):
            if registration.name in result["behaviors"]:
                continue
            fields = self._fields(registration.interface)
            if fields:
                result["behaviors"][registration.name] = fields
        return result
