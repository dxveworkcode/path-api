import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_EVENT_PATTERN = re.compile(r"/event/([A-Za-z0-9]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    event = _EVENT_PATTERN.search(parsed.path)
    if event:
        event_id = event.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"ticketmaster://event/{event_id}",
            app_name="Ticketmaster",
            platform="ticketmaster",
            extracted_id=event_id,
        )
    raise InvalidURLError("Could not resolve this Ticketmaster URL. Expected /event/{id}.")
