import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ARTIST_PATTERN = re.compile(r"/artist/([A-Za-z0-9]+)")
_ALBUM_PATTERN = re.compile(r"/album/([A-Za-z0-9]+)")
_TRACK_PATTERN = re.compile(r"/track/([A-Za-z0-9]+)")
_PLAYLIST_PATTERN = re.compile(r"/playlist/([A-Za-z0-9]+)")


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
                scheme=f"tidal://{entity_type}/{entity_id}",
                app_name="Tidal",
                platform="tidal",
                extracted_id=entity_id,
            )
    raise InvalidURLError("Could not resolve this Tidal URL. Expected /track/, /album/, /artist/, or /playlist/.")
