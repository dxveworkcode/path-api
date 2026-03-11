import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_CHANNEL_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")
_CLIP_PATTERN = re.compile(r"^/clip/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    clip = _CLIP_PATTERN.match(parsed.path)
    if clip:
        clip_id = clip.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"twitch://clip/{clip_id}",
            app_name="Twitch",
            platform="twitch",
            extracted_id=clip_id,
        )
    channel = _CHANNEL_PATTERN.match(parsed.path)
    if channel and channel.group(1) not in ("directory", "p", "downloads", "jobs"):
        channel_name = channel.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"twitch://open/?stream={channel_name}",
            app_name="Twitch",
            platform="twitch",
            extracted_id=channel_name,
        )
    raise InvalidURLError("Could not resolve this Twitch URL. Expected /{channel} or /clip/{id}.")
