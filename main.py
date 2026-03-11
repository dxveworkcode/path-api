import html
import json 
import os
from urllib.parse import urlparse

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Header, HTTPException

from core.exceptions import (
    InvalidURLError,
    UnsupportedAppError,
    invalid_url_handler,
    unsupported_app_handler,
)
from core.models import ResolveResponse
from resolvers.registry import RESOLVER_MAP

RAPID_SECRET = os.environ.get("RAPIDAPI_PROXY_SECRET", "")

app = FastAPI(
    title="Path DeepLink API",
    description="Resolve standard web URLs into mobile deep-link schemes.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.add_exception_handler(InvalidURLError, invalid_url_handler)
app.add_exception_handler(UnsupportedAppError, unsupported_app_handler)


@app.exception_handler(Exception)
async def generic_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"error": "internal_error", "detail": "An unexpected error occurred."},
    )

@app.middleware("http")
async def require_rapidapi(request, call_next):
    if RAPID_SECRET:
        secret = request.headers.get("X-RapidAPI-Proxy-Secret")
        if secret != RAPID_SECRET:
            return JSONResponse({"error": "forbidden"}, status_code=403)
    return await call_next(request)


@app.get(
    "/v1/resolve",
    response_model=ResolveResponse,
    summary="Resolve a web URL to a deep-link scheme",
    tags=["Resolve"],
)
async def resolve_url(
    url: str = Query(..., description="The full web URL to resolve, e.g. https://open.spotify.com/track/4cOdK2wGLETKBW3PvgPWqT"),
) -> ResolveResponse:
    parsed = urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        raise InvalidURLError(
            f"'{url}' is not a valid URL. Include the full scheme, e.g. https://..."
        )

    host = parsed.netloc.lower()
    resolver = RESOLVER_MAP.get(host)

    if resolver is None:
        raise UnsupportedAppError(host)

    return resolver(parsed)


@app.get("/v1/apps", tags=["Meta"], summary="List all supported apps and their hostnames")
async def list_apps() -> dict:
    apps: dict[str, list[str]] = {}
    for host, fn in RESOLVER_MAP.items():
        module = fn.__module__.split(".")[-1].capitalize()
        apps.setdefault(module, []).append(host)
    return {"supported_apps": apps}


def _open_page(app_name: str, scheme: str) -> str:
    safe_name = html.escape(app_name)
    scheme_js = json.dumps(scheme)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Opening {safe_name}\u2026</title>
<style>
body{{font-family:system-ui,-apple-system,sans-serif;background:#080910;color:#E8EAED;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  min-height:100svh;margin:0;text-align:center;padding:1.5rem;gap:0.5rem;}}
h1{{font-size:1.2rem;font-weight:700;margin:0;}}
p{{color:#7A8290;font-size:0.85rem;margin:0;}}
.btn{{display:inline-block;margin-top:1.4rem;background:#3D7EFF;color:#fff;
  padding:0.75rem 1.8rem;border-radius:8px;text-decoration:none;
  font-weight:700;font-size:0.9rem;}}
</style>
</head>
<body>
<h1>Opening {safe_name}\u2026</h1>
<p>If the app doesn\u2019t open automatically, tap the button.</p>
<a class="btn" id="btn">Open {safe_name}</a>
<script>var s={scheme_js};document.getElementById('btn').href=s;setTimeout(function(){{window.location.href=s;}},80);</script>
</body>
</html>"""


@app.get(
    "/v1/open",
    response_class=HTMLResponse,
    summary="Resolve a web URL and redirect to the native app",
    tags=["Resolve"],
)
async def open_url(
    url: str = Query(..., description="The full web URL to open in its native app"),
) -> HTMLResponse:
    parsed = urlparse(url)

    if not parsed.scheme or not parsed.netloc:
        raise InvalidURLError(
            f"'{url}' is not a valid URL. Include the full scheme, e.g. https://..."
        )

    host = parsed.netloc.lower()
    resolver = RESOLVER_MAP.get(host)

    if resolver is None:
        raise UnsupportedAppError(host)

    result = resolver(parsed)
    return HTMLResponse(content=_open_page(result.app_name, result.scheme))


app.mount("/", StaticFiles(directory="static", html=True), name="static")

