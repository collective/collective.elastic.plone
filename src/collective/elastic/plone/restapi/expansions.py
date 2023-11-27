from Acquisition import aq_base
from plone import api
from plone.restapi.behaviors import IBlocks
from plone.restapi.indexers import extract_text
from plone.restapi.interfaces import IExpandableElement
from zope.annotation import IAnnotations
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface


@implementer(IExpandableElement)
@adapter(Interface, Interface)
class CollectiveElastic:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def _getBlocksPlainText(self, obj):
        """Extract text from blocks and subblocks."""
        request = getRequest()
        blocks = aq_base(obj).blocks
        blocks_layout = aq_base(obj).blocks_layout
        blocks_text = []
        for block_id in blocks_layout.get("items", []):
            block = blocks.get(block_id, {})
            blocks_text.append(extract_text(block, obj, request))

        return " ".join([text.strip() for text in blocks_text if text.strip()])

    def __call__(self, expand=False):
        result = {
            "collectiveelastic": {
                "@id": f"{self.context.absolute_url()}/@collectiveelastic"
            }
        }
        if not expand:
            return result

        # rid
        catalog = api.portal.get_tool("portal_catalog")
        path = "/".join(self.context.getPhysicalPath())
        rid = catalog.getrid(path)

        # timestamp
        annotations = IAnnotations(self.context)
        if annotations is None:
            return {}
        ts = annotations.get("ELASTIC_LAST_INDEXING_QUEUED_TIMESTAMP", 0)

        # allowedRolesAndUsers
        index = catalog._catalog.getIndex("allowedRolesAndUsers")

        result["collectiveelastic"].update(
            {
                "catalog_rid": rid,
                "last_indexing_queued": ts,
                "allowedRolesAndUsers": index.getEntryForObject(rid, default=[]),
            }
        )
        # blocks_plaintext - only for Volto, not for ClassicUI
        # or Dexterity types w/o blocks behavior
        if IBlocks.providedBy(self.context):
            result["blocks_plaintext"] = self._getBlocksPlainText(self.context)
        return result
