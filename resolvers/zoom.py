import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_MEETING_PATTERN = re.compile(r"/j/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    meeting = _MEETING_PATTERN.search(parsed.path)
    if meeting:
        meeting_id = meeting.group(1)
        params = parse_qs(parsed.query)
        pwd = params.get("pwd", [None])[0]
        scheme = f"zoommtg://zoom.us/join?confno={meeting_id}"
        if pwd:
            scheme += f"&pwd={pwd}"
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=scheme,
            app_name="Zoom",
            platform="zoom",
            extracted_id=meeting_id,
        )
    raise InvalidURLError("Could not resolve this Zoom URL. Expected zoom.us/j/{meeting_id}.")
