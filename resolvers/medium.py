import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")
_POST_PATTERN = re.compile(r"/([A-Za-z0-9_]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"medium://p/{username}",
            app_name="Medium",
            platform="medium",
            extracted_id=username,
        )
    # /username/post-slug-hexid — extract the hex post ID from the end
    post_id_match = re.search(r"-([a-f0-9]+)$", parsed.path)
    if post_id_match:
        post_id = post_id_match.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"medium://p/{post_id}",
            app_name="Medium",
            platform="medium",
            extracted_id=post_id,
        )
    raise InvalidURLError("Could not resolve this Medium URL.")
