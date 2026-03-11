import re
from urllib.parse import ParseResult, parse_qs

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_SHORTLINK_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)$")
_CHANNEL_ID_PATTERN = re.compile(r"^/channel/([A-Za-z0-9_-]+)")
_HANDLE_PATTERN = re.compile(r"^/@([A-Za-z0-9_.-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    host = parsed.netloc.lower()
    path = parsed.path

    # youtu.be short links
    if host in ("youtu.be",):
        match = _SHORTLINK_PATTERN.match(path)
        if match:
            video_id = match.group(1)
            return ResolveResponse(
                url=parsed.geturl(),
                scheme=f"vnd.youtube:{video_id}",
                app_name="YouTube",
                platform="youtube",
                extracted_id=video_id,
            )

    # /watch?v=VIDEO_ID
    if path == "/watch":
        params = parse_qs(parsed.query)
        video_ids = params.get("v")
        if video_ids:
            video_id = video_ids[0]
            return ResolveResponse(
                url=parsed.geturl(),
                scheme=f"vnd.youtube:{video_id}",
                app_name="YouTube",
                platform="youtube",
                extracted_id=video_id,
            )

    # /channel/CHANNEL_ID
    channel_match = _CHANNEL_ID_PATTERN.match(path)
    if channel_match:
        channel_id = channel_match.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"youtube://www.youtube.com/channel/{channel_id}",
            app_name="YouTube",
            platform="youtube",
            extracted_id=channel_id,
        )

    # /@handle
    handle_match = _HANDLE_PATTERN.match(path)
    if handle_match:
        handle = handle_match.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"youtube://www.youtube.com/@{handle}",
            app_name="YouTube",
            platform="youtube",
            extracted_id=handle,
        )

    raise InvalidURLError(
        "Could not resolve this YouTube URL. "
        "Supported patterns: /watch?v=, youtu.be/{id}, /channel/{id}, /@handle."
    )
