import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_PRODUCT_PATTERN = re.compile(r"/p/([A-Za-z0-9-]+)/([A-Za-z0-9]+)")
_SEARCH_PATTERN = re.compile(r"^/s/")


def resolve(parsed: ParseResult) -> ResolveResponse:
    product = _PRODUCT_PATTERN.search(parsed.path)
    if product:
        product_id = product.group(2)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"target://product/{product_id}",
            app_name="Target",
            platform="target",
            extracted_id=product_id,
        )
    if _SEARCH_PATTERN.match(parsed.path):
        return ResolveResponse(
            url=parsed.geturl(),
            scheme="target://search",
            app_name="Target",
            platform="target",
            extracted_id=None,
        )
    raise InvalidURLError("Could not resolve this Target URL. Expected /p/{name}/{id}.")
