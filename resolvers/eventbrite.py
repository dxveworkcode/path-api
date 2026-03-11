import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_EVENT_PATTERN = re.compile(r"/event/([A-Za-z0-9_-]+)-(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    event = _EVENT_PATTERN.search(parsed.path)
    if event:
        event_id = event.group(2)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"eventbrite://event/{event_id}",
            app_name="Eventbrite",
            platform="eventbrite",
            extracted_id=event_id,
        )
    raise InvalidURLError("Could not resolve this Eventbrite URL. Expected /event/{name}-{id}.")
