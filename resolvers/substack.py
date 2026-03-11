import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")
_POST_PATTERN = re.compile(r"^/p/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    post = _POST_PATTERN.match(parsed.path)
    if post:
        post_slug = post.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"substack://post/{post_slug}",
            app_name="Substack",
            platform="substack",
            extracted_id=post_slug,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"substack://profile/{username}",
            app_name="Substack",
            platform="substack",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Substack URL.")
