import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_CONTENT_PATTERN = re.compile(r"/content/([A-Za-z0-9_-]+)")
_SERIES_PATTERN = re.compile(r"/series/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    series = _SERIES_PATTERN.search(parsed.path)
    if series:
        series_id = series.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"disneyplus://series/{series_id}",
            app_name="Disney+",
            platform="disney_plus",
            extracted_id=series_id,
        )
    content = _CONTENT_PATTERN.search(parsed.path)
    if content:
        content_id = content.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"disneyplus://content/{content_id}",
            app_name="Disney+",
            platform="disney_plus",
            extracted_id=content_id,
        )
    raise InvalidURLError("Could not resolve this Disney+ URL.")
