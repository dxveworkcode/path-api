import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_PHONE_PATTERN = re.compile(r"^/([0-9]+)/?$")


def resolve(parsed: ParseResult) -> ResolveResponse:
    phone = _PHONE_PATTERN.match(parsed.path)
    if phone:
        phone_number = phone.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"whatsapp://send?phone={phone_number}",
            app_name="WhatsApp",
            platform="whatsapp",
            extracted_id=phone_number,
        )
    raise InvalidURLError("Could not resolve this WhatsApp URL. Expected wa.me/{phone_number}.")
