import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_HOTEL_PATTERN = re.compile(r"/hotel/([A-Za-z0-9_-]+\.\w+\.html)")
_SEARCH_PATTERN = re.compile(r"^/searchresults")


def resolve(parsed: ParseResult) -> ResolveResponse:
    hotel = _HOTEL_PATTERN.search(parsed.path)
    if hotel:
        hotel_slug = hotel.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"booking://hotel/{hotel_slug}",
            app_name="Booking.com",
            platform="booking",
            extracted_id=hotel_slug,
        )
    if _SEARCH_PATTERN.match(parsed.path):
        return ResolveResponse(
            url=parsed.geturl(),
            scheme="booking://search",
            app_name="Booking.com",
            platform="booking",
            extracted_id=None,
        )
    raise InvalidURLError("Could not resolve this Booking.com URL.")
