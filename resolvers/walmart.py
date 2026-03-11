import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_PRODUCT_PATTERN = re.compile(r"/ip/(?:[A-Za-z0-9_-]+/)?(\d+)")
_SEARCH_PATTERN = re.compile(r"^/search")


def resolve(parsed: ParseResult) -> ResolveResponse:
    product = _PRODUCT_PATTERN.search(parsed.path)
    if product:
        product_id = product.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"walmart://product/{product_id}",
            app_name="Walmart",
            platform="walmart",
            extracted_id=product_id,
        )
    if _SEARCH_PATTERN.match(parsed.path):
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"walmart://search?query={parsed.query}",
            app_name="Walmart",
            platform="walmart",
            extracted_id=None,
        )
    raise InvalidURLError("Could not resolve this Walmart URL. Expected /ip/{id}.")
