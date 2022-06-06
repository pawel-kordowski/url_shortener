from __future__ import annotations

from dataclasses import dataclass

from app.models.url import Url as UrlModel


@dataclass
class Url:
    short_url: str
    full_url: str

    @classmethod
    def from_model(cls, model_instance: UrlModel) -> Url:
        return cls(
            short_url=model_instance.short_url,
            full_url=model_instance.full_url,
        )
