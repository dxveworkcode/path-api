from urllib.parse import urlparse

from fastapi import FastAPI, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from core.exceptions import (
    InvalidURLError,
    UnsupportedAppError,
    invalid_url_handler,
    unsupported_app_handler,
)
from core.models import ResolveResponse
from resolvers.registry import RESOLVER_MAP

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


app.mount("/", StaticFiles(directory="static", html=True), name="static")
