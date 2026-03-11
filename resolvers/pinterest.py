import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_PIN_PATTERN = re.compile(r"/pin/(\d+)")
_USER_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/?$")
_BOARD_PATTERN = re.compile(r"^/([A-Za-z0-9_]+)/([A-Za-z0-9_-]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    pin = _PIN_PATTERN.search(parsed.path)
    if pin:
        pin_id = pin.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"pinterest://pin/{pin_id}",
            app_name="Pinterest",
            platform="pinterest",
            extracted_id=pin_id,
        )
    board = _BOARD_PATTERN.match(parsed.path)
    if board:
        user, board_name = board.group(1), board.group(2)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"pinterest://board/{user}/{board_name}",
            app_name="Pinterest",
            platform="pinterest",
            extracted_id=f"{user}/{board_name}",
        )
    user = _USER_PATTERN.match(parsed.path)
    if user:
        username = user.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"pinterest://user/{username}",
            app_name="Pinterest",
            platform="pinterest",
            extracted_id=username,
        )
    raise InvalidURLError("Could not resolve this Pinterest URL.")
