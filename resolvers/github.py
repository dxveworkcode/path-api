import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_REPO_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)/([A-Za-z0-9_.-]+)/?$")
_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    repo = _REPO_PATTERN.match(parsed.path)
    if repo:
        owner, repo_name = repo.group(1), repo.group(2)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"github://repo/{owner}/{repo_name}",
            app_name="GitHub",
            platform="github",
            extracted_id=f"{owner}/{repo_name}",
        )
    user = _USER_PATTERN.match(parsed.path)
    if user and user.group(1) not in ("explore", "topics", "trending", "marketplace"):
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"github://user/{username}",
            app_name="GitHub",
            platform="github",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this GitHub URL.")
