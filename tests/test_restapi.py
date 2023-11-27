from collective.elastic.plone.testing import COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

import unittest


def FakeRequest(dict):
    pass


class TestRestAPI(unittest.TestCase):
    layer = COLLECTIVE_ES_PLONE_INTEGRATION_TESTING

    def test_schema_api(self):
        self.maxDiff = None
        from collective.elastic.plone.restapi.schema import SchemaService

        result = SchemaService().reply()
        expected = {
            "behaviors": {
                "plone.allowdiscussion": [
                    {
                        "field": "zope.schema._field.Choice",
                        "languages": ["en"],
                        "name": "allow_discussion",
                    }
                ],
                "plone.basic": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "title",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "description",
                    },
                ],
                "plone.categorization": [
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "subjects",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    },
                    {
                        "field": "zope.schema._field.Choice",
                        "languages": ["en"],
                        "name": "language",
                    },
                ],
                "plone.collection": [
                    {
                        "field": "zope.schema._field.List",
                        "languages": ["en"],
                        "name": "query",
                        "value_type": {
                            "field": "zope.schema._field.Dict",
                            "languages": ["en"],
                            "value_type": {
                                "field": "zope.schema._bootstrapfields.Field",
                                "languages": ["en"],
                            },
                        },
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "sort_on",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "sort_reversed",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Int",
                        "languages": ["en"],
                        "name": "limit",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Int",
                        "languages": ["en"],
                        "name": "item_count",
                    },
                    {
                        "field": "zope.schema._field.List",
                        "languages": ["en"],
                        "name": "customViewFields",
                        "value_type": {
                            "field": "zope.schema._field.Choice",
                            "languages": ["en"],
                        },
                    },
                ],
                "plone.dublincore": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "title",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "description",
                    },
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "subjects",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    },
                    {
                        "field": "zope.schema._field.Choice",
                        "languages": ["en"],
                        "name": "language",
                    },
                    {
                        "field": "zope.schema._field.Datetime",
                        "languages": ["en"],
                        "name": "effective",
                    },
                    {
                        "field": "zope.schema._field.Datetime",
                        "languages": ["en"],
                        "name": "expires",
                    },
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "creators",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    },
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "contributors",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "rights",
                    },
                ],
                "plone.eventattendees": [
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "attendees",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    }
                ],
                "plone.eventbasic": [
                    {
                        "field": "zope.schema._field.Datetime",
                        "languages": ["en"],
                        "name": "start",
                    },
                    {
                        "field": "zope.schema._field.Datetime",
                        "languages": ["en"],
                        "name": "end",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "whole_day",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "open_end",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "sync_uid",
                    },
                ],
                "plone.eventcontact": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "contact_name",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "contact_email",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "contact_phone",
                    },
                    {
                        "field": "zope.schema._field.URI",
                        "languages": ["en"],
                        "name": "event_url",
                    },
                ],
                "plone.eventlocation": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "location",
                    }
                ],
                "plone.eventrecurrence": [
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "recurrence",
                    }
                ],
                "plone.excludefromnavigation": [
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "exclude_from_nav",
                    }
                ],
                "plone.leadimage": [
                    {
                        "field": "plone.namedfile.field.NamedBlobImage",
                        "languages": ["en"],
                        "name": "image",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "image_caption",
                    },
                ],
                "plone.namefromtitle": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "title",
                    }
                ],
                "plone.nextprevioustoggle": [
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "nextPreviousEnabled",
                    }
                ],
                "plone.ownership": [
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "creators",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    },
                    {
                        "field": "zope.schema._field.Tuple",
                        "languages": ["en"],
                        "name": "contributors",
                        "value_type": {
                            "field": "zope.schema._bootstrapfields.TextLine",
                            "languages": ["en"],
                        },
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "rights",
                    },
                ],
                "plone.publication": [
                    {
                        "field": "zope.schema._field.Datetime",
                        "languages": ["en"],
                        "name": "effective",
                    },
                    {
                        "field": "zope.schema._field.Datetime",
                        "languages": ["en"],
                        "name": "expires",
                    },
                ],
                "plone.relateditems": [
                    {
                        "field": "z3c.relationfield.schema.RelationList",
                        "languages": ["en"],
                        "name": "relatedItems",
                        "value_type": {
                            "field": "z3c.relationfield.schema.RelationChoice",
                            "languages": ["en"],
                        },
                    }
                ],
                "plone.richtext": [
                    {
                        "field": "plone.app.textfield.RichText",
                        "languages": ["en"],
                        "name": "text",
                    }
                ],
                "plone.shortname": [
                    {
                        "field": "zope.schema._field.ASCIILine",
                        "languages": ["en"],
                        "name": "id",
                    }
                ],
                "plone.tableofcontents": [
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "table_of_contents",
                    }
                ],
                "plone.thumb_icon": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "thumb_scale_list",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "thumb_scale_table",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "thumb_scale_summary",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "suppress_icons",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "suppress_thumbs",
                    },
                ],
                "plone.versioning": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "changeNote",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Bool",
                        "languages": ["en"],
                        "name": "versioning_enabled",
                    },
                ],
                "volto.blocks": [
                    {
                        "field": "plone.schema.jsonfield.JSONField",
                        "languages": ["en"],
                        "name": "blocks",
                    },
                    {
                        "field": "plone.schema.jsonfield.JSONField",
                        "languages": ["en"],
                        "name": "blocks_layout",
                    },
                ],
                "volto.blocks.editable.layout": [
                    {
                        "field": "plone.schema.jsonfield.JSONField",
                        "languages": ["en"],
                        "name": "blocks",
                    },
                    {
                        "field": "plone.schema.jsonfield.JSONField",
                        "languages": ["en"],
                        "name": "blocks_layout",
                    },
                ],
            },
            "types": {
                "File": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "title",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "description",
                    },
                    {
                        "field": "plone.namedfile.field.NamedBlobFile",
                        "languages": ["en"],
                        "name": "file",
                    },
                ],
                "Image": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "title",
                    },
                    {
                        "field": "zope.schema._bootstrapfields.Text",
                        "languages": ["en"],
                        "name": "description",
                    },
                    {
                        "field": "plone.namedfile.field.NamedBlobImage",
                        "languages": ["en"],
                        "name": "image",
                    },
                ],
                "Link": [
                    {
                        "field": "zope.schema._bootstrapfields.TextLine",
                        "languages": ["en"],
                        "name": "remoteUrl",
                    }
                ],
            },
        }

        breakpoint()
        self.assertEqual(result, expected)
