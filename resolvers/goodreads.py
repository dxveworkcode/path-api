import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_BOOK_PATTERN = re.compile(r"/book/show/(\d+)")
_AUTHOR_PATTERN = re.compile(r"/author/show/(\d+)")
_LIST_PATTERN = re.compile(r"/list/show/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    book = _BOOK_PATTERN.search(parsed.path)
    if book:
        book_id = book.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"goodreads://book/{book_id}",
            app_name="Goodreads",
            platform="goodreads",
            extracted_id=book_id,
        )
    author = _AUTHOR_PATTERN.search(parsed.path)
    if author:
        author_id = author.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"goodreads://author/{author_id}",
            app_name="Goodreads",
            platform="goodreads",
            extracted_id=author_id,
        )
    raise InvalidURLError("Could not resolve this Goodreads URL.")
