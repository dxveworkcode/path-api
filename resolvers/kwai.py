import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_VIDEO_PATTERN = re.compile(r"/video/(\d+)")
_USER_PATTERN = re.compile(r"^/@?([A-Za-z0-9_.]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    video = _VIDEO_PATTERN.search(parsed.path)
    if video:
        video_id = video.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"kwai://video/{video_id}",
            app_name="Kwai",
            platform="kwai",
            extracted_id=video_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"kwai://user/{username}",
            app_name="Kwai",
            platform="kwai",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Kwai URL.")
