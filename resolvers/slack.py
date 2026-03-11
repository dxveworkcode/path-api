import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_CHANNEL_PATTERN = re.compile(r"^/t/([A-Za-z0-9_]+)/?\?workspaceSlug=([A-Za-z0-9_-]+)")
_WORKSPACE_PATTERN = re.compile(r"^/([A-Za-z0-9_-]+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    workspace = _WORKSPACE_PATTERN.match(parsed.path)
    if workspace:
        workspace_slug = workspace.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"slack://open?team={workspace_slug}",
            app_name="Slack",
            platform="slack",
            extracted_id=workspace_slug,
        )
    raise InvalidURLError("Could not resolve this Slack URL.")
