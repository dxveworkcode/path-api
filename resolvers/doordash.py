import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_RESTAURANT_PATTERN = re.compile(r"/store/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    restaurant = _RESTAURANT_PATTERN.search(parsed.path)
    if restaurant:
        store_id = restaurant.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"doordash://store/{store_id}",
            app_name="DoorDash",
            platform="doordash",
            extracted_id=store_id,
        )
    raise InvalidURLError("Could not resolve this DoorDash URL. Expected /store/{id}.")
