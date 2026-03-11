from urllib.parse import ParseResult

from core.models import ResolveResponse


def resolve(parsed: ParseResult) -> ResolveResponse:
    return ResolveResponse(
        url=parsed.geturl(),
        scheme="uber://",
        app_name="Uber",
        platform="uber",
        extracted_id=None,
    )
