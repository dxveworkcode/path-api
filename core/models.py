from pydantic import BaseModel, HttpUrl


class ResolveResponse(BaseModel):
    url: str
    scheme: str
    app_name: str
    platform: str
    extracted_id: str | None = None
