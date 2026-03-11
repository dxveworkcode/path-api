import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_CHANNEL_PATTERN = re.compile(r"^/channel/([A-Za-z0-9_-]+)")
_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    params = parse_qs(parsed.query)
    video_ids = params.get("v")
    if video_ids:
        video_id = video_ids[0]
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"vimeo://app.vimeo.com/videos/{video_id}",
            app_name="Vimeo",
            platform="vimeo",
            extracted_id=video_id,
        )
    channel = _CHANNEL_PATTERN.match(parsed.path)
    if channel:
        channel_id = channel.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"vimeo://app.vimeo.com/channels/{channel_id}",
            app_name="Vimeo",
            platform="vimeo",
            extracted_id=channel_id,
        )
    # Direct numeric video ID in path: vimeo.com/123456789
    video_path = re.match(r"^/(\d+)/?$", parsed.path)
    if video_path:
        video_id = video_path.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"vimeo://app.vimeo.com/videos/{video_id}",
            app_name="Vimeo",
            platform="vimeo",
            extracted_id=video_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"vimeo://app.vimeo.com/user/{username}",
            app_name="Vimeo",
            platform="vimeo",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Vimeo URL.")
