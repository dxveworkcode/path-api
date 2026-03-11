import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_PROFILE_PATTERN = re.compile(r"^/in/([A-Za-z0-9_-]+)")
_COMPANY_PATTERN = re.compile(r"^/company/([A-Za-z0-9_-]+)")
_POST_PATTERN = re.compile(r"/posts/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    post = _POST_PATTERN.search(parsed.path)
    if post:
        post_id = post.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"linkedin://posts/{post_id}",
            app_name="LinkedIn",
            platform="linkedin",
            extracted_id=post_id,
        )
    company = _COMPANY_PATTERN.match(parsed.path)
    if company:
        company_slug = company.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"linkedin://company/{company_slug}",
            app_name="LinkedIn",
            platform="linkedin",
            extracted_id=company_slug,
        )
    profile = _PROFILE_PATTERN.match(parsed.path)
    if profile:
        profile_id = profile.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"linkedin://profile/{profile_id}",
            app_name="LinkedIn",
            platform="linkedin",
            extracted_id=profile_id,
        )
    raise InvalidURLError("Could not resolve this LinkedIn URL.")
