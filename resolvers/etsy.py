import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_LISTING_PATTERN = re.compile(r"/listing/(\d+)")
_SHOP_PATTERN = re.compile(r"/shop/([A-Za-z0-9_]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    listing = _LISTING_PATTERN.search(parsed.path)
    if listing:
        listing_id = listing.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"etsy://listing/{listing_id}",
            app_name="Etsy",
            platform="etsy",
            extracted_id=listing_id,
        )
    shop = _SHOP_PATTERN.search(parsed.path)
    if shop:
        shop_name = shop.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"etsy://shop/{shop_name}",
            app_name="Etsy",
            platform="etsy",
            extracted_id=shop_name,
        )
    raise InvalidURLError("Could not resolve this Etsy URL. Expected /listing/{id} or /shop/{name}.")
