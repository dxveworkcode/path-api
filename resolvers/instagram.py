import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_POST_PATTERN = re.compile(r"^/p/([A-Za-z0-9_-]+)")
_REEL_PATTERN = re.compile(r"^/reel/([A-Za-z0-9_-]+)")
_PROFILE_PATTERN = re.compile(r"^/([A-Za-z0-9_.]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    path = parsed.path.rstrip("/")

    post_match = _POST_PATTERN.match(path)
    if post_match:
        media_id = post_match.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"instagram://media?id={media_id}",
            app_name="Instagram",
            platform="instagram",
            extracted_id=media_id,
        )

    reel_match = _REEL_PATTERN.match(path)
    if reel_match:
        reel_id = reel_match.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"instagram://reels/videos/{reel_id}",
            app_name="Instagram",
            platform="instagram",
            extracted_id=reel_id,
        )

    profile_match = _PROFILE_PATTERN.match(path)
    if profile_match:
        username = profile_match.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"instagram://user?username={username}",
            app_name="Instagram",
            platform="instagram",
            extracted_id=username,
        )

    raise InvalidURLError(
        "Could not resolve this Instagram URL. "
        "Supported patterns: /p/{id}, /reel/{id}, /{username}."
    )
