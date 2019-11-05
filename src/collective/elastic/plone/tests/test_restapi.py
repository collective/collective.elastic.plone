# -*- coding: utf-8 -*-
from collective.elastic.plone.testing import COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

import unittest


def FakeRequest(dict):
    pass


class TestRestAPI(unittest.TestCase):
    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def test_schema_api(self):
        from collective.elastic.plone.restapi.schema import SchemaService

        result = SchemaService().reply()
        expected = {
            "behaviors": {
                "plone.allowdiscussion": [
                    {"field": "zope.schema._field.Choice", "name": "allow_discussion"}
                ],
                "plone.basic": [
                    {"field": "zope.schema._bootstrapfields.TextLine", "name": "title"},
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "name": "description",
                    },
                ],
                "plone.categorization": [
                    {"field": "zope.schema._field.Tuple", "name": "subjects"},
                    {"field": "zope.schema._field.Choice", "name": "language"},
                ],
                "plone.collection": [
                    {"field": "zope.schema._field.List", "name": "query"},
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "sort_on",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "sort_reversed",
                    },
                    {"field": "zope.schema._bootstrapfields.Int", "name": "limit"},
                    {"field": "zope.schema._bootstrapfields.Int", "name": "item_count"},
                    {"field": "zope.schema._field.List", "name": "customViewFields"},
                ],
                "plone.dublincore": [
                    {"field": "zope.schema._bootstrapfields.TextLine", "name": "title"},
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "name": "description",
                    },
                    {"field": "zope.schema._field.Tuple", "name": "subjects"},
                    {"field": "zope.schema._field.Choice", "name": "language"},
                    {"field": "zope.schema._field.Datetime", "name": "effective"},
                    {"field": "zope.schema._field.Datetime", "name": "expires"},
                    {"field": "zope.schema._field.Tuple", "name": "creators"},
                    {"field": "zope.schema._field.Tuple", "name": "contributors"},
                    {"field": "zope.schema._bootstrapfields.Text", "name": "rights"},
                ],
                "plone.eventattendees": [
                    {"field": "zope.schema._field.Tuple", "name": "attendees"}
                ],
                "plone.eventbasic": [
                    {"field": "zope.schema._field.Datetime", "name": "start"},
                    {"field": "zope.schema._field.Datetime", "name": "end"},
                    {"field": "zope.schema._bootstrapfields.Bool", "name": "whole_day"},
                    {"field": "zope.schema._bootstrapfields.Bool", "name": "open_end"},
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "sync_uid",
                    },
                ],
                "plone.eventcontact": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "contact_name",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "contact_email",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "contact_phone",
                    },
                    {"field": "zope.schema._field.URI", "name": "event_url"},
                ],
                "plone.eventlocation": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "location",
                    }
                ],
                "plone.eventrecurrence": [
                    {"field": "zope.schema._bootstrapfields.Text", "name": "recurrence"}
                ],
                "plone.excludefromnavigation": [
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "exclude_from_nav",
                    }
                ],
                "plone.leadimage": [
                    {"field": "plone.namedfile.field.NamedBlobImage", "name": "image"},
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "image_caption",
                    },
                ],
                "plone.namefromtitle": [
                    {"field": "zope.schema._bootstrapfields.TextLine", "name": "title"}
                ],
                "plone.nextprevioustoggle": [
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "nextPreviousEnabled",
                    }
                ],
                "plone.ownership": [
                    {"field": "zope.schema._field.Tuple", "name": "creators"},
                    {"field": "zope.schema._field.Tuple", "name": "contributors"},
                    {"field": "zope.schema._bootstrapfields.Text", "name": "rights"},
                ],
                "plone.publication": [
                    {"field": "zope.schema._field.Datetime", "name": "effective"},
                    {"field": "zope.schema._field.Datetime", "name": "expires"},
                ],
                "plone.relateditems": [
                    {
                        "field": "z3c.relationfield.schema.RelationList",
                        "name": "relatedItems",
                    }
                ],
                "plone.richtext": [
                    {"field": "plone.app.textfield.RichText", "name": "text"}
                ],
                "plone.shortname": [
                    {"field": "zope.schema._field.ASCIILine", "name": "id"}
                ],
                "plone.tableofcontents": [
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "table_of_contents",
                    }
                ],
                "plone.thumb_icon": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "thumb_scale_list",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "thumb_scale_table",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "thumb_scale_summary",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "suppress_icons",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "suppress_thumbs",
                    },
                ],
                "plone.tiles": [
                    {"field": "plone.schema.jsonfield.JSONField", "name": "tiles"},
                    {
                        "field": "plone.schema.jsonfield.JSONField",
                        "name": "tiles_layout",
                    },
                ],
                "plone.versioning": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "changeNote",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "name": "versioning_enabled",
                    },
                ],
            },
            "types": {
                "File": [
                    {"field": "zope.schema._bootstrapfields.TextLine", "name": "title"},
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "name": "description",
                    },
                    {"field": "plone.namedfile.field.NamedBlobFile", "name": "file"},
                ],
                "Image": [
                    {"field": "zope.schema._bootstrapfields.TextLine", "name": "title"},
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "name": "description",
                    },
                    {"field": "plone.namedfile.field.NamedBlobImage", "name": "image"},
                ],
                "Link": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "name": "remoteUrl",
                    }
                ],
            },
        }
        self.assertEqual(result, expected)
