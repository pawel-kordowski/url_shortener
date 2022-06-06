from app.domain import entities
from app.domain.repositories.base import PostgresRepository


class UrlRepository(PostgresRepository):
    async def create_url(self, short_url: str, full_url: str) -> entities.Url:
        pass

    async def get_url_by_short(self, short_url: str) -> entities.Url | None:
        pass

    async def is_short_url_taken(self, short_url: str) -> bool:
        pass
