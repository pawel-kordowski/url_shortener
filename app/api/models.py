import validators
from pydantic import BaseModel, validator


class UrlInput(BaseModel):
    url: str

    @validator("url")
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Invalid URL")
        return v


class UrlOutput(BaseModel):
    full_url: str
    short_url: str
