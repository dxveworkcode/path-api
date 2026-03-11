import re
from urllib.parse import ParseResult

from core.exceptions import InvalidURLError
from core.models import ResolveResponse

_ACTIVITY_PATTERN = re.compile(r"/activities/(\d+)")
_ATHLETE_PATTERN = re.compile(r"/athletes/(\d+)")
_SEGMENT_PATTERN = re.compile(r"/segments/(\d+)")


def resolve(parsed: ParseResult) -> ResolveResponse:
    activity = _ACTIVITY_PATTERN.search(parsed.path)
    if activity:
        activity_id = activity.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"strava://activities/{activity_id}",
            app_name="Strava",
            platform="strava",
            extracted_id=activity_id,
        )
    athlete = _ATHLETE_PATTERN.search(parsed.path)
    if athlete:
        athlete_id = athlete.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"strava://athletes/{athlete_id}",
            app_name="Strava",
            platform="strava",
            extracted_id=athlete_id,
        )
    segment = _SEGMENT_PATTERN.search(parsed.path)
    if segment:
        segment_id = segment.group(1)
        return ResolveResponse(
            url=parsed.geturl(),
            scheme=f"strava://segments/{segment_id}",
            app_name="Strava",
            platform="strava",
            extracted_id=segment_id,
        )
    raise InvalidURLError("Could not resolve this Strava URL.")
