import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ITEM_PATTERN = re.compile(r"/itm/(?:[A-Za-z0-9_-]+/)?(\d+)")
_USER_PATTERN = re.compile(r"/usr/([A-Za-z0-9_]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    item = _ITEM_PATTERN.search(parsed.path)
    if item:
        item_id = item.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"ebay://launch?nav=item.view&id={item_id}",
            app_name="eBay",
            platform="ebay",
            extracted_id=item_id,
        )
    user = _USER_PATTERN.search(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"ebay://launch?nav=profile&id={username}",
            app_name="eBay",
            platform="ebay",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this eBay URL. Expected /itm/{id} or /usr/{username}.")
