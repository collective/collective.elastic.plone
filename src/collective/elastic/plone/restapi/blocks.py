from plone.restapi.behaviors import IBlocks
from plone.restapi.blocks import visit_subblocks
from plone.restapi.indexers import extract_text
from plone.restapi.interfaces import IBlockSearchableText
from zope.component import adapter
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserRequest


@implementer(IBlockSearchableText)
@adapter(IBlocks, IBrowserRequest)
class AccordionBlockSearchableText:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block_value):
        result = ""
        for subblock in visit_subblocks(self.context, block_value):
            if "title" in subblock:
                subblock_title = subblock["title"]
                if not isinstance(subblock_title, str):
                    subblock_title = str(subblock_title)
                result = f"{result}\n{subblock_title}"
            subblock_result = extract_text(subblock, self.context, self.request)
            result = f"{result} {subblock_result}"
        return result


@implementer(IBlockSearchableText)
@adapter(IBlocks, IBrowserRequest)
class TeaserBlockSearchableText:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, block_value):
        result = ""
        if "head_title" in block_value:
            if block_value["head_title"]:
                result = f"{result}\n{block_value['head_title']}"
        if "title" in block_value:
            if block_value["title"]:
                result = f"{result}\n{block_value['title']}"
        if "description" in block_value:
            if block_value["description"]:
                result = f"{result}\n{block_value['description']}"
        return result
