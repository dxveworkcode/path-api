import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")
_MOMENT_PATTERN = re.compile(r"/moments/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    moment = _MOMENT_PATTERN.search(parsed.path)
    if moment:
        moment_id = moment.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"berealmobile://moments/{moment_id}",
            app_name="BeReal",
            platform="bereal",
            extracted_id=moment_id,
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"berealmobile://user/{username}",
            app_name="BeReal",
            platform="bereal",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this BeReal URL.")
