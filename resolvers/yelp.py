import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_BIZ_PATTERN = re.compile(r"/biz/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    biz = _BIZ_PATTERN.search(parsed.path)
    if biz:
        alias = biz.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"yelp://biz/{alias}",
            app_name="Yelp",
            platform="yelp",
            extracted_id=alias,
        )
    raise InvalidURLError("Could not resolve this Yelp URL. Expected /biz/{alias}.")
