elasticsearchresponse = """
{
    "took": 58,
    "timed_out": false,
    "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 2,
            "relation": "eq"
        },
        "max_score": 3.7457137,
        "hits": [
            {
                "_index": "plone",
                "_id": "e21e3141ac144f20bf52f06a67a1bf8d",
                "_score": 3.7457137,
                "_source": {
                    "parent": {
                        "image_scales": null,
                        "@type": "Document",
                        "description": "Pages with meta data \"Informationtype\"",
                        "@id": "http://localhost:8080/Plone/example-content",
                        "title": "Example Content",
                        "image_field": null,
                        "review_state": "private"
                    },
                    "@type": "Document",
                    "creators": [
                        "admin"
                    ],
                    "language": {
                        "title": "English",
                        "token": "en"
                    },
                    "title": "Schwimmen von Sommer zu Sommer",
                    "rid": 1388221493,
                    "portal_type": "Document",
                    "informationtype": [
                        {
                            "title": "News Item",
                            "token": "newsitem"
                        }
                    ],
                    "effective": "2022-11-13T15:05:53",
                    "allow_discussion": false,
                    "lock": {
                        "creator": "admin",
                        "created": "2022-11-13T16:18:27.286568",
                        "name": "plone.locking.stealable",
                        "stealable": true,
                        "creator_name": "admin",
                        "creator_url": "http://localhost:8080/Plone/author/admin",
                        "time": 1668352707.286568,
                        "locked": true,
                        "timeout": 600,
                        "token": "0.5602870987873713-0.7996039360206804-00105A989226:1668352707.287"
                    },
                    "modified": "2022-11-13T15:18:42+00:00",
                    "@id": "http://localhost:8080/Plone/example-content/swimming-from-summer-to-summer",
                    "id": "swimming-from-summer-to-summer",
                    "blocks_plaintext": "Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Morbi leo risus, porta ac consectetur ac, vestibulum at eros.  So das war der Sommer schon fast.  Donec id elit non mi porta gravida at eget metus. Vestibulum id ligula porta felis euismod semper.\r\rSed posuere consectetur est at lobortis. Duis mollis, est non commodo luctus, .",
                    "created": "2022-11-13T14:05:47+00:00",
                    "review_state": "published",
                    "is_folderish": true,
                    "layout": "document_view",
                    "UID": "e21e3141ac144f20bf52f06a67a1bf8d",
                    "exclude_from_nav": false
                },
                "highlight": {
                    "blocks_plaintext": [
                        "consectetur ac, vestibulum at eros.  So das war der <em>Sommer</em> schon fast.  Donec id elit non mi porta gravida"
                    ],
                    "title": [
                        "Schwimmen von <em>Sommer</em> zu <em>Sommer</em>"
                    ]
                }
            },
            {
                "_index": "plone",
                "_id": "4996ecdbd0874662918dca6800af4e20",
                "_score": 0.2576383,
                "_source": {
                    "parent": {
                        "image_scales": null,
                        "@type": "Document",
                        "description": "Pages with meta data \"Informationtype\"",
                        "@id": "http://localhost:8080/Plone/example-content",
                        "title": "Example Content",
                        "image_field": null,
                        "review_state": "private"
                    },
                    "@type": "Document",
                    "creators": [
                        "admin"
                    ],
                    "description": "The november on the roof top garden",
                    "language": {
                        "title": "English",
                        "token": "en"
                    },
                    "title": "Gärtnern auf dem Dach im November",
                    "rid": 1388221492,
                    "portal_type": "Document",
                    "informationtype": [
                        {
                            "title": "Questions and Answers",
                            "token": "qanda"
                        },
                        {
                            "title": "News Item",
                            "token": "newsitem"
                        }
                    ],
                    "effective": "2022-11-13T12:10:57",
                    "allow_discussion": false,
                    "lock": {
                        "creator": "admin",
                        "created": "2022-11-13T16:19:06.430420",
                        "name": "plone.locking.stealable",
                        "stealable": true,
                        "creator_name": "admin",
                        "creator_url": "http://localhost:8080/Plone/author/admin",
                        "time": 1668352746.43042,
                        "locked": true,
                        "timeout": 600,
                        "token": "0.09177211796461515-0.27278992806491165-00105A989226:1668352746.430"
                    },
                    "modified": "2022-11-13T15:19:20+00:00",
                    "@id": "http://localhost:8080/Plone/example-content/gardening-on-the-roof-top-in-november",
                    "id": "gardening-on-the-roof-top-in-november",
                    "blocks_plaintext": "Dachbegrünung mit Gemüse: Welche Vorteile gibt es?  Der Gemüseanbau auf dem Dach bietet daher Menschen, die sonst keine Möglichkeit hätten, zu gärtnern, eben diese. Gerade Kindern  kann so nähergebracht werden, dass Gemüse eigentlich nicht aus der  Kaufhalle stammt. Aber auch Erwachsenen wird der Wert von Lebensmitteln  so wieder bewusster.  Wer Gemüse  auf dem Dach anbaut, nutzt Kleinstflächen optimal aus. Das ist gerade  in Städten von Vorteil, wo nur sehr eingeschränkt andere Anbauflächen  vorhanden sind. Die Dachbegrünung mit Gemüse ist somit zwar kein Ersatz  für die Landwirtschaft, dafür aber eine sinnvolle Ergänzung.  Weiter im nächsten Sommer.",
                    "created": "2022-11-13T11:10:13+00:00",
                    "review_state": "published",
                    "is_folderish": true,
                    "layout": "document_view",
                    "UID": "4996ecdbd0874662918dca6800af4e20",
                    "exclude_from_nav": false
                },
                "highlight": {
                    "blocks_plaintext": [
                        "aber eine sinnvolle Ergänzung.  Weiter im nächsten <em>Sommer</em>."
                    ]
                }
            }
        ]
    },
    "aggregations": {
        "informationtype_agg": {
            "meta": {},
            "doc_count": 2,
            "inner": {
                "doc_count": 3,
                "informationtype_token": {
                    "doc_count_error_upper_bound": 0,
                    "sum_other_doc_count": 0,
                    "buckets": [
                        {
                            "key": "newsitem",
                            "doc_count": 2,
                            "somemoredatafromelasticsearch": {
                                "hits": {
                                    "total": {
                                        "value": 2,
                                        "relation": "eq"
                                    },
                                    "max_score": 3.7457137,
                                    "hits": [
                                        {
                                            "_index": "plone",
                                            "_id": "e21e3141ac144f20bf52f06a67a1bf8d",
                                            "_nested": {
                                                "field": "informationtype",
                                                "offset": 0
                                            },
                                            "_score": 3.7457137,
                                            "_source": {
                                                "title": "News Item",
                                                "token": "newsitem"
                                            }
                                        }
                                    ]
                                }
                            }
                        },
                        {
                            "key": "qanda",
                            "doc_count": 1,
                            "somemoredatafromelasticsearch": {
                                "hits": {
                                    "total": {
                                        "value": 1,
                                        "relation": "eq"
                                    },
                                    "max_score": 0.2576383,
                                    "hits": [
                                        {
                                            "_index": "plone",
                                            "_id": "4996ecdbd0874662918dca6800af4e20",
                                            "_nested": {
                                                "field": "informationtype",
                                                "offset": 0
                                            },
                                            "_score": 0.2576383,
                                            "_source": {
                                                "title": "Questions and Answers",
                                                "token": "qanda"
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    ]
                }
            }
        }
    }
}
"""
