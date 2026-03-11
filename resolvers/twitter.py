import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_TWEET_PATTERN = re.compile(r"/(?:status|i/web/status)/(\d+)")
_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    tweet = _TWEET_PATTERN.search(parsed.path)
    if tweet:
        tweet_id = tweet.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"twitter://status?id={tweet_id}",
            app_name="X (Twitter)",
            platform="twitter",
            extracted_id=tweet_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"twitter://user?screen_name={username}",
            app_name="X (Twitter)",
            platform="twitter",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this X/Twitter URL. Expected /{username} or /status/{id}.")
