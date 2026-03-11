import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_TITLE_PATTERN = re.compile(r"/title/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    title = _TITLE_PATTERN.search(parsed.path)
    if title:
        title_id = title.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"nflx://www.netflix.com/title/{title_id}",
            app_name="Netflix",
            platform="netflix",
            extracted_id=title_id,
        )
    raise InvalidURLError("Could not resolve this Netflix URL. Expected /title/{id}.")
