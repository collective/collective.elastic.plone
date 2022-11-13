voltorequest = """
{
    "url": "http://localhost:9200",
    "index": "plone",
    "query": {
        "query": {
            "bool": {
                "should": [
                    {
                        "query_string": {
                            "query": "Sommer Sommer~",
                            "fields": [
                                "title^1.4",
                                "description^1.2",
                                "blocks_plaintext"
                            ]
                        }
                    }
                ],
                "must": [],
                "must_not": []
            }
        },
        "highlight": {
            "number_of_fragments": 20,
            "fields": [
                {
                    "title": {
                        "matched_fields": [
                            "title",
                            "title.exact"
                        ],
                        "type": "fvh"
                    }
                },
                {
                    "description": {
                        "matched_fields": [
                            "description",
                            "description.exact"
                        ],
                        "type": "fvh"
                    }
                },
                {
                    "blocks_plaintext": {
                        "matched_fields": [
                            "blocks_plaintext",
                            "blocks_plaintext.exact"
                        ],
                        "type": "fvh"
                    }
                }
            ]
        },
        "size": 10,
        "from": 0,
        "post_filter": {
            "bool": {
                "must": [
                    {
                        "terms": {
                            "portal_type": [
                                "Document"
                            ]
                        }
                    },
                    {
                        "terms": {
                            "review_state": [
                                "published"
                            ]
                        }
                    }
                ],
                "filter": [
                    {
                        "nested": {
                            "path": "informationtype",
                            "query": {
                                "bool": {
                                    "must": [
                                        {
                                            "terms": {
                                                "informationtype.token": [
                                                    "newsitem"
                                                ]
                                            }
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        },
        "aggs": {
            "informationtype_agg": {
                "aggs": {
                    "inner": {
                        "nested": {
                            "path": "informationtype"
                        },
                        "aggs": {
                            "informationtype_token": {
                                "terms": {
                                    "field": "informationtype.token",
                                    "order": {
                                        "_key": "asc"
                                    },
                                    "size": 30
                                },
                                "aggs": {
                                    "somemoredatafromelasticsearch": {
                                        "top_hits": {
                                            "size": 1,
                                            "_source": {
                                                "includes": [
                                                    "informationtype"
                                                ]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "filter": {
                    "bool": {
                        "filter": []
                    }
                }
            }
        }
    }
}
"""
