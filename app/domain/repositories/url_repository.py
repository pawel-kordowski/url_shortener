from sqlalchemy import select

from app.domain import entities
from app.domain.repositories.base import PostgresRepository
from app.models.url import Url


class UrlRepository(PostgresRepository):
    async def create_url(self, short_url: str, full_url: str) -> entities.Url:
        url = Url(short_url=short_url, full_url=full_url)
        self.session.add(url)
        await self.session.commit()
        return entities.Url.from_model(url)

    async def get_url_by_short(self, short_url: str) -> entities.Url | None:
        query = select(Url).where(Url.short_url == short_url)

        results = (await self.session.execute(query)).first()

        if results:
            result = results[0]
            return entities.Url.from_model(result)

    async def is_short_url_taken(self, short_url: str) -> bool:
        url = await self.get_url_by_short(short_url=short_url)

        return url is not None
