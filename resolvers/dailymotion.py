import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_VIDEO_PATTERN = re.compile(r"/video/([A-Za-z0-9_-]+)")
_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    video = _VIDEO_PATTERN.search(parsed.path)
    if video:
        video_id = video.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"dailymotion://video/{video_id}",
            app_name="Dailymotion",
            platform="dailymotion",
            extracted_id=video_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user and user.group(1) not in ("browse", "search", "trending"):
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"dailymotion://user/{username}",
            app_name="Dailymotion",
            platform="dailymotion",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Dailymotion URL.")
