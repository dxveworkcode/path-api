import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_TRACK_PATTERN = re.compile(r"/track/(\d+)")
_ARTIST_PATTERN = re.compile(r"/artist/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    track = _TRACK_PATTERN.search(parsed.path)
    if track:
        track_id = track.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"shazam://track/{track_id}",
            app_name="Shazam",
            platform="shazam",
            extracted_id=track_id,
        )
    artist = _ARTIST_PATTERN.search(parsed.path)
    if artist:
        artist_id = artist.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"shazam://artist/{artist_id}",
            app_name="Shazam",
            platform="shazam",
            extracted_id=artist_id,
        )
    raise InvalidURLError("Could not resolve this Shazam URL. Expected /track/{id} or /artist/{id}.")
