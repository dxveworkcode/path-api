import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ITUNES_ID_PATTERN = re.compile(r"/id(\d+)")
_SHOW_PATTERN = re.compile(r"/show/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    itunes_id = _ITUNES_ID_PATTERN.search(parsed.path)
    if itunes_id:
        content_id = itunes_id.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"videos://tv.apple.com/content/{content_id}",
            app_name="Apple TV",
            platform="apple_tv",
            extracted_id=content_id,
        )
    show = _SHOW_PATTERN.search(parsed.path)
    if show:
        show_id = show.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"videos://tv.apple.com/show/{show_id}",
            app_name="Apple TV",
            platform="apple_tv",
            extracted_id=show_id,
        )
    raise InvalidURLError("Could not resolve this Apple TV URL.")
