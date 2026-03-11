import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ROOM_PATTERN = re.compile(r"/rooms/(\d+)")
_EXPERIENCE_PATTERN = re.compile(r"/experiences/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    room = _ROOM_PATTERN.search(parsed.path)
    if room:
        room_id = room.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"airbnb://rooms/{room_id}",
            app_name="Airbnb",
            platform="airbnb",
            extracted_id=room_id,
        )
    experience = _EXPERIENCE_PATTERN.search(parsed.path)
    if experience:
        experience_id = experience.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"airbnb://experiences/{experience_id}",
            app_name="Airbnb",
            platform="airbnb",
            extracted_id=experience_id,
        )
    raise InvalidURLError("Could not resolve this Airbnb URL. Expected /rooms/{id} or /experiences/{id}.")
