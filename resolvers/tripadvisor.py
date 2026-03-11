import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ATTRACTION_PATTERN = re.compile(r"/Attraction_Review-[^/]+-d(\d+)-")
_HOTEL_PATTERN = re.compile(r"/Hotel_Review-[^/]+-d(\d+)-")
_RESTAURANT_PATTERN = re.compile(r"/Restaurant_Review-[^/]+-d(\d+)-")


def resolve(parsed: ParseResult) -> ResolveResponse:
    for pattern, entity_type in [
        (_ATTRACTION_PATTERN, "attraction"),
        (_HOTEL_PATTERN, "hotel"),
        (_RESTAURANT_PATTERN, "restaurant"),
    ]:
        match = pattern.search(parsed.path)
        if match:
            entity_id = match.group(1)
            return ResolveResponse(
                url=parsed.geturl(),
                scheme=f"tripadvisor://{entity_type}/{entity_id}",
                app_name="Tripadvisor",
                platform="tripadvisor",
                extracted_id=entity_id,
            )
    raise InvalidURLError("Could not resolve this Tripadvisor URL.")
