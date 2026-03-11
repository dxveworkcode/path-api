import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_SUBREDDIT_PATTERN = re.compile(r"^/r/([A-Za-z0-9_]+)")
_POST_PATTERN = re.compile(r"/r/[A-Za-z0-9_]+/comments/([A-Za-z0-9]+)")
_USER_PATTERN = re.compile(r"^/u(?:ser)?/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    post = _POST_PATTERN.search(parsed.path)
    if post:
        post_id = post.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"reddit://reddit.com/comments/{post_id}",
            app_name="Reddit",
            platform="reddit",
            extracted_id=post_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"reddit://reddit.com/user/{username}",
            app_name="Reddit",
            platform="reddit",
            extracted_id=username,
        )
    subreddit = _SUBREDDIT_PATTERN.match(parsed.path)
    if subreddit:
        sub_name = subreddit.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"reddit://reddit.com/r/{sub_name}",
            app_name="Reddit",
            platform="reddit",
            extracted_id=sub_name,
        )
    raise InvalidURLError("Could not resolve this Reddit URL.")
