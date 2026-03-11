import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_THREAD_PATTERN = re.compile(r"^/t/([A-Za-z0-9]+)")
_USER_PATTERN = re.compile(r"^/@?([A-Za-z0-9_]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    thread = _THREAD_PATTERN.match(parsed.path)
    if thread:
        thread_id = thread.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"threads://thread?id={thread_id}",
            app_name="Threads",
            platform="threads",
            extracted_id=thread_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"threads://user?username={username}",
            app_name="Threads",
            platform="threads",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Threads URL. Expected /@{username} or /t/{id}.")
