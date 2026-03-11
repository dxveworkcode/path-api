from urllib.parse import ParseResult

from core.models import ResolveResponse


def resolve(parsed: ParseResult) -> ResolveResponse:
    return ResolveResponse(
        url=parsed.geturl(),
        scheme="lyft://ridetype?id=lyft",
        app_name="Lyft",
        platform="lyft",
        extracted_id=None,
    )
