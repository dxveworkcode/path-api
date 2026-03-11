import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_SNAP_PATTERN = re.compile(r"^/add/([A-Za-z0-9_.]+)")
_STORY_PATTERN = re.compile(r"^/stories/([A-Za-z0-9_.]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    snap = _SNAP_PATTERN.match(parsed.path)
    if snap:
        username = snap.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"snapchat://add/{username}",
            app_name="Snapchat",
            platform="snapchat",
            extracted_id=username,
        )
    story = _STORY_PATTERN.match(parsed.path)
    if story:
        username = story.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"snapchat://story/{username}",
            app_name="Snapchat",
            platform="snapchat",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Snapchat URL. Expected /add/{username} or /stories/{username}.")
