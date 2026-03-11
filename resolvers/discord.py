import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_INVITE_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)/?$")
_CHANNEL_PATTERN = re.compile(r"^/channels/(\d+)/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    channel = _CHANNEL_PATTERN.match(parsed.path)
    if channel:
        guild_id, channel_id = channel.group(1), channel.group(2)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"discord://discord.com/channels/{guild_id}/{channel_id}",
            app_name="Discord",
            platform="discord",
            extracted_id=guild_id,
        )
    invite = _INVITE_PATTERN.match(parsed.path)
    if invite:
        invite_code = invite.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"discord://discord.com/invite/{invite_code}",
            app_name="Discord",
            platform="discord",
            extracted_id=invite_code,
        )
    raise InvalidURLError("Could not resolve this Discord URL.")
