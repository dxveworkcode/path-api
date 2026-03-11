import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_TELEGRAM_TG_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")
_JOINCHAT_PATTERN = re.compile(r"^/joinchat/([A-Za-z0-9_-]+)")
_PLUS_PATTERN = re.compile(r"^\+([0-9]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    # t.me/+XXXXX is an invite link
    plus = _PLUS_PATTERN.match(parsed.path.lstrip("/"))
    if plus:
        invite_hash = plus.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"tg://join?invite={invite_hash}",
            app_name="Telegram",
            platform="telegram",
            extracted_id=invite_hash,
        )
    joinchat = _JOINCHAT_PATTERN.match(parsed.path)
    if joinchat:
        invite_hash = joinchat.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"tg://join?invite={invite_hash}",
            app_name="Telegram",
            platform="telegram",
            extracted_id=invite_hash,
        )
    user = _TELEGRAM_TG_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"tg://resolve?domain={username}",
            app_name="Telegram",
            platform="telegram",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Telegram URL.")
