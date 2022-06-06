import validators
from pydantic import BaseModel, validator


class UrlInput(BaseModel):
    url: str

    @validator("url")
    def validate_url(cls, url: str) -> str:
        if not validators.url(url):
            raise ValueError("Invalid URL")
        return url


class UrlOutput(BaseModel):
    full_url: str
    short_url: str
