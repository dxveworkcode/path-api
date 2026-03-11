import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_TRACK_PATTERN = re.compile(r"/track/(\d+)")
_ALBUM_PATTERN = re.compile(r"/album/(\d+)")
_ARTIST_PATTERN = re.compile(r"/artist/(\d+)")
_PLAYLIST_PATTERN = re.compile(r"/playlist/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    for pattern, entity_type in [
        (_TRACK_PATTERN, "track"),
        (_ALBUM_PATTERN, "album"),
        (_ARTIST_PATTERN, "artist"),
        (_PLAYLIST_PATTERN, "playlist"),
    ]:
        match = pattern.search(parsed.path)
        if match:
            entity_id = match.group(1)
            return ResolveResponse(
                url=parsed.geturl(),
                scheme=f"deezer://{entity_type}/{entity_id}",
                app_name="Deezer",
                platform="deezer",
                extracted_id=entity_id,
            )
    raise InvalidURLError("Could not resolve this Deezer URL.")
