import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ASIN_PATTERN = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})")


def resolve(parsed: ParseResult) -> ResolveResponse:
    match = _ASIN_PATTERN.search(parsed.path)
    if not match:
        raise InvalidURLError(
            "Could not extract an ASIN from this Amazon URL. "
            "Expected a path like /dp/B08N5WRWNW or /gp/product/B08N5WRWNW."
        )
    asin = match.group(1)
    return ResolveResponse(
        url=parsed.geturl(),
        scheme=f"amzn://dp/{asin}",
        app_name="Amazon",
        platform="amazon",
        extracted_id=asin,
    )
