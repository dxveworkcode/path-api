from fastapi import Request
from fastapi.responses import JSONResponse


class InvalidURLError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class UnsupportedAppError(Exception):
    def __init__(self, host: str) -> None:
        self.host = host
        self.message = f"No deep-link resolver found for '{host}'. Check /v1/apps for the supported list."
        super().__init__(self.message)


async def invalid_url_handler(request: Request, exc: InvalidURLError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"error": "invalid_url", "detail": exc.message},
    )


async def unsupported_app_handler(request: Request, exc: UnsupportedAppError) -> JSONResponse:
    return JSONResponse(
        status_code=404,
        content={"error": "unsupported_app", "detail": exc.message},
    )
