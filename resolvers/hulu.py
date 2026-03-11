import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_VIDEO_PATTERN = re.compile(r"/watch/([A-Za-z0-9_-]+)")
_SERIES_PATTERN = re.compile(r"/series/([A-Za-z0-9_-]+)/")


def resolve(parsed: ParseResult) -> ResolveResponse:
    video = _VIDEO_PATTERN.search(parsed.path)
    if video:
        video_id = video.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"hulu://www.hulu.com/watch/{video_id}",
            app_name="Hulu",
            platform="hulu",
            extracted_id=video_id,
        )
    series = _SERIES_PATTERN.search(parsed.path)
    if series:
        series_id = series.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"hulu://www.hulu.com/series/{series_id}",
            app_name="Hulu",
            platform="hulu",
            extracted_id=series_id,
        )
    raise InvalidURLError("Could not resolve this Hulu URL. Expected /watch/{id} or /series/{id}/.")
