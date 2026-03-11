import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_VIDEO_PATTERN = re.compile(r"/@[^/]+/video/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    match = _VIDEO_PATTERN.search(parsed.path)
    if not match:
        raise InvalidURLError(
            "Could not extract a video ID from this TikTok URL. "
            "Expected a path like /@username/video/7123456789."
        )
    video_id = match.group(1)
    return ResolveResponse(
        url=parsed.geturl(),
        scheme=f"snssdk1128://aweme/detail/{video_id}",
        app_name="TikTok",
        platform="tiktok",
        extracted_id=video_id,
    )
