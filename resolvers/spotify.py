import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_PATH_PATTERN = re.compile(r"^/(track|album|artist|playlist)/([A-Za-z0-9]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    match = _PATH_PATTERN.match(parsed.path)
    if not match:
        raise InvalidURLError(
            "Could not resolve this Spotify URL. "
            "Supported patterns: /track/{id}, /album/{id}, /artist/{id}, /playlist/{id}."
        )
    entity_type = match.group(1)
    entity_id = match.group(2)
    return ResolveResponse(
        url=parsed.geturl(),
        scheme=f"spotify:{entity_type}:{entity_id}",
        app_name="Spotify",
        platform="spotify",
        extracted_id=entity_id,
    )
