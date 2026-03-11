from urllib.parse import ParseResult

from core.models import ResolveResponse


def resolve(parsed: ParseResult) -> ResolveResponse:
    return ResolveResponse(
        url=parsed.geturl(),
        scheme="duolingo://",
        app_name="Duolingo",
        platform="duolingo",
        extracted_id=None,
    )
