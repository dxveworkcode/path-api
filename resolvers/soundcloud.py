import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_TRACK_PATTERN = re.compile(r"/tracks/(\d+)")
_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)/?$")
_PLAYLIST_PATTERN = re.compile(r"/([A-Za-z0-9_-]+)/sets/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    track = _TRACK_PATTERN.search(parsed.path)
    if track:
        track_id = track.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"soundcloud://tracks/{track_id}",
            app_name="SoundCloud",
            platform="soundcloud",
            extracted_id=track_id,
        )
    playlist = _PLAYLIST_PATTERN.match(parsed.path)
    if playlist:
        user, slug = playlist.group(1), playlist.group(2)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"soundcloud://playlists/{user}/{slug}",
            app_name="SoundCloud",
            platform="soundcloud",
            extracted_id=f"{user}/{slug}",
        )
    user = _USER_PATTERN.match(parsed.path)
    if user and user.group(1) not in ("discover", "stream", "search", "you"):
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"soundcloud://users/{username}",
            app_name="SoundCloud",
            platform="soundcloud",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this SoundCloud URL.")
