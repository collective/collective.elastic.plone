from . import INDEX_NAME
from AccessControl import ClassSecurityInfo
from AccessControl.class_init import InitializeClass
from AccessControl.requestmethod import postonly
from BTrees.IIBTree import IIBTree
from collective.elastic.ingest import OPENSEARCH
from collective.elastic.ingest.client import get_client
from OFS.SimpleItem import SimpleItem
from plone import api
from pprint import pformat
from Products.GenericSetup.interfaces import ISetupEnviron
from Products.GenericSetup.utils import NodeAdapterBase
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluginIndexes.interfaces import ISortIndex
from Products.ZCatalog.query import IndexQuery
from zope.component import adapter
from zope.interface import implementer

import jinja2
import json
import logging


if OPENSEARCH:
    from opensearchpy.exceptions import RequestError
    from opensearchpy.exceptions import TransportError
else:
    from elasticsearch.exceptions import RequestError
    from elasticsearch.exceptions import TransportError


logger = logging.getLogger(__name__)

jinja_loader = jinja2.Environment(loader=jinja2.BaseLoader)

VIEW_PERMISSION = "View"
MGMT_PERMISSION = "Manage ZCatalogIndex Entries"

manage_addESPIndexForm = PageTemplateFile("www/addIndex", globals())

BATCH_SIZE = 500

LANGUAGE_TO_ANALYZER = {
    # available plone language codes see
    # https://github.com/plone/plone.i18n/blob/master/plone/i18n/locales/languages.py
    # please add more languages mappings here, if them apply
    # language analyzers are the available ones in Open-/ElasticSearch
    "ar": "arabic",
    "hy": "armenian",
    "eu": "basque",
    "bn": "bengali",
    "pt-br": "brazilian",
    "bg": "bulgarian",
    "ca": "catalan",
    "cz": "czech",
    "da": "danish",
    "nl": "dutch",
    "en": "english",
    "et": "estonian",
    "fi": "finnish",
    "fr": "french",
    "gl": "galician",
    "de": "german",
    "el": "greek",
    "hi": "hindi",
    "hu": "hungarian",
    "id": "indonesian",
    "ga": "irish",
    "it": "italian",
    "la": "latvian",
    "lt": "lithuanian",
    "no": "norwegian",
    "fa": "persian",
    "pt": "portuguese",
    "ro": "romanian",
    "ru": "russian",
    "ku": "sorani",  # Kurdish dialect
    "es": "spanish",
    "se": "swedish",
    "tr": "turkish",
    "th": "thai",
}

# Hint for my future self: When copying this code, never name it
# manage_addIndex here. Otherwise install will be broken.
# There is some serious namespace pollution in Zope.App.FactoryDispatcher


def manage_addESPIndex(context, id, extra=None, REQUEST=None, RESPONSE=None, URL3=None):
    """Adds a date range in range index"""
    result = context.manage_addIndex(
        id,
        "ElasticSearchProxyIndex",
        extra=extra,
        REQUEST=REQUEST,
        RESPONSE=RESPONSE,
        URL1=URL3,
    )
    return result


@implementer(ISortIndex)
class ElasticSearchProxyIndex(SimpleItem):
    meta_type = "ElasticSearchProxyIndex"
    security = ClassSecurityInfo()

    query_options = ("query",)

    manage_main = PageTemplateFile("www/manageIndex", globals())
    manage_options = ({"label": "Settings", "action": "manage_main"},)

    def __init__(self, id, ignore_ex=None, call_methods=None, extra=None, caller=None):
        self.id = id
        self.caller = caller
        if extra is None:
            return
        try:
            self.query_template = extra.query_template
        except AttributeError:
            try:
                # alternative: allow a dict (lowers bootstrapping effort
                # from code)
                self.query_template = extra["query_template"]
            except KeyError:
                raise ValueError(
                    'ElasticSearchProxyIndex needs "extra" kwarg with key or '
                    'attribute "query_template".'
                )

    @security.protected(MGMT_PERMISSION)
    @postonly
    def manage_ESPIndexExtras(self, REQUEST):
        """stores changed extras"""
        self.query_template = REQUEST.form["extra"]["query_template"]
        REQUEST["RESPONSE"].redirect(
            "{}/manage_catalogIndexes?manage_tabs_message=Updated "
            "index settings for {}".format(self.aq_parent.absolute_url(), self.id)
        )

    ###########################################################################
    # Methods we dont need to implement, from IPluginIndex.
    # Those operations are done in the queue processor in a more efficinet way.
    ###########################################################################

    def index_object(self, documentId, obj, threshold=None):
        return 0

    def unindex_object(self, documentId):
        pass

    def clear(self):
        pass

    ###########################################################################
    #  methods from IPluginIndex
    ###########################################################################

    def getEntryForObject(self, documentId, default=None):
        """Get all information contained for 'documentId'.

        We could fetch here the tika converted text field from ES and return it.

        Future.
        """
        return ""

    def getIndexSourceNames(self):
        """Get a sequence of attribute names that are indexed by the index.
        return sequence of indexed attributes

        """
        # Future: here we could fiddle with the ES query to get the attributes.
        #         For now, we just return the index name.
        return [self.id]

    def getIndexQueryNames(self):
        """Get a sequence of query parameter names to which this index applies.

        Note: Needed for query plan.

        Indicate that this index applies to queries for the index's name.
        """
        return (self.id,)

    def _apply_index(self, request):
        """Apply the index to query parameters given in 'request'.

        The argument should be a mapping object.

        If the request does not contain the needed parameters, then
        None is returned.

        If the request contains a parameter with the name of the
        column and this parameter is either a Record or a class
        instance then it is assumed that the parameters of this index
        are passed as attribute (Note: this is the recommended way to
        pass parameters since Zope 2.4)

        Otherwise two objects are returned.  The first object is a
        ResultSet containing the record numbers of the matching
        records.  The second object is a tuple containing the names of
        all data fields used.
        """
        logger.debug(f"*** _apply_index {self.id}")
        record = IndexQuery(request, self.id)
        if record.keys is None:
            return None
        keys = []
        for key in record.keys:
            key = key.replace("\\", "").replace('"', "").replace("*", "")
            key = key.replace(" AND ", " ").replace(" OR ", " ")
            keys.append(key)
        current_language = api.portal.get_current_language()
        analyzer = LANGUAGE_TO_ANALYZER.get(current_language, None)
        if analyzer is None:
            if "-" in current_language:
                main_language = current_language.split("-")[0]
                analyzer = LANGUAGE_TO_ANALYZER.get(main_language, "standard")
            else:
                analyzer = "standard"
        template_params = {
            "keys": keys,
            "language": current_language,
            "analyzer": analyzer,
        }
        __traceback_info__ = "template parameters: {}".format(template_params)
        query_body = self._apply_template(template_params)
        logger.debug(f"query_body : {query_body}")
        search = dict(
            index=INDEX_NAME,
            body=query_body,
            size=BATCH_SIZE,
            scroll="1m",
            _source_includes=["rid"],
        )
        if api.env.debug_mode():
            search["_source_includes"].append("@id")
        client = get_client()
        try:
            result = client.search(**search)
        except RequestError:
            logger.warn(f"Query failed:\n{query_body}")
            return None
        except TransportError:
            logger.exception("ElasticSearch failed")
            return None
        logger.debug(f"Response Open-/ElasticSearch:\n{result}")
        # initial return value, other batches to be applied

        retval = IIBTree()

        def _handle_records(records):
            for record in records:
                # map rid to score
                retval[record["_source"]["rid"]] = int(10000 * float(record["_score"]))

        _handle_records(result["hits"]["hits"])

        total = result["hits"]["total"]["value"]
        if total > BATCH_SIZE:
            sid = result["_scroll_id"]
            counter = BATCH_SIZE
            while counter < total:
                result = client.scroll(scroll_id=sid, scroll="1m")
                _handle_records(result["hits"]["hits"])
                counter += BATCH_SIZE
        return retval, (self.id,)

    def numObjects(self):
        """Return the number of indexed objects."""
        es_kwargs = dict(index=INDEX_NAME, body={"query": {"match_all": {}}})
        try:
            client = get_client()
            return client.count(**es_kwargs)["count"]
        except Exception:
            logger.exception('ElasticSearch "count" query failed')
            return "Problem getting all documents count from Open-/ ElasticSearch!"

    @security.protected(MGMT_PERMISSION)
    def external_index_mapping(self):
        """Return the settings of the os/es index."""
        try:
            client = get_client()
            mapping = client.indices.get_mapping(index=INDEX_NAME)
        except Exception:
            logger.exception('Open-/ ElasticSearch "get_mapping" query failed')
            return f"Problem getting mapping for index {INDEX_NAME} from Open-/ ElasticSearch!"
        return pformat(mapping[INDEX_NAME]["mappings"]["properties"], indent=2)

    @security.protected(MGMT_PERMISSION)
    def external_index_name(self):
        """Return the name of the os/es index."""
        return INDEX_NAME

    def indexSize(self):
        """Return the size of the index in terms of distinct values."""
        return "n/a"

    ###########################################################################
    #  methods coming from ISortIndex
    ###########################################################################

    def keyForDocument(self, documentId):
        """Return the sort key that cooresponds to the specified document id

        This method is no longer used by ZCatalog, but is left for backwards
        compatibility."""
        # We do not implement this BBB method.
        pass

    def documentToKeyMap(self):
        """Return an object that supports __getitem__ and may be used to
        quickly lookup the sort key given a document id"""

        # We can not implement this afaik

    ###########################################################################
    #  private helper methods
    ###########################################################################

    def _apply_template(self, template_data):
        query_template = self.query_template
        if isinstance(query_template, bytes):
            query_template = query_template.decode("utf8")
        tpl = jinja_loader.from_string(query_template)
        query_text = tpl.render(template_data)
        return json.loads(query_text)


InitializeClass(ElasticSearchProxyIndex)


@adapter(ElasticSearchProxyIndex, ISetupEnviron)
class IndexNodeAdapter(NodeAdapterBase):
    """Node im- and exporter for Index."""

    @property
    def node(self):
        """Export the object as a DOM node."""
        node = self._getObjectNode("index")
        child = self._doc.createElement("querytemplate")
        text = self._doc.createTextNode(self.context.query_template)
        child.appendChild(text)
        node.appendChild(child)
        return node

    @node.setter
    def node(self, node):
        """Import the object from the DOM node."""
        child_nodes = [
            x
            for x in node.childNodes
            if x.nodeType == 1 and x.nodeName == "querytemplate"
        ]
        if child_nodes:
            text_node = child_nodes[0].childNodes[0]
            self.context.query_template = text_node.data.encode("utf-8")
        else:
            self.context.query_template = "{}"  # noqa: P103
