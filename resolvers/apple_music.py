import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ARTIST_PATTERN = re.compile(r"/artist/(\d+)")
_ALBUM_PATTERN = re.compile(r"/album/(\d+)")
_SONG_PATTERN = re.compile(r"/song/(\d+)")
_PLAYLIST_PATTERN = re.compile(r"/playlist/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    song = _SONG_PATTERN.search(parsed.path)
    if song:
        song_id = song.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"music://song/{song_id}",
            app_name="Apple Music",
            platform="apple_music",
            extracted_id=song_id,
        )
    album = _ALBUM_PATTERN.search(parsed.path)
    if album:
        album_id = album.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"music://album/{album_id}",
            app_name="Apple Music",
            platform="apple_music",
            extracted_id=album_id,
        )
    artist = _ARTIST_PATTERN.search(parsed.path)
    if artist:
        artist_id = artist.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"music://artist/{artist_id}",
            app_name="Apple Music",
            platform="apple_music",
            extracted_id=artist_id,
        )
    playlist = _PLAYLIST_PATTERN.search(parsed.path)
    if playlist:
        playlist_id = playlist.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"music://playlist/{playlist_id}",
            app_name="Apple Music",
            platform="apple_music",
            extracted_id=playlist_id,
        )
    raise InvalidURLError("Could not resolve this Apple Music URL.")
