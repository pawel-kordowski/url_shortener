from app import config
from app.domain import entities
from app.domain.random_string_generator import RandomStringGenerator
from app.domain.repositories.url_repository import UrlRepository


class UrlService:
    @classmethod
    async def create_url(cls, full_url: str) -> entities.Url:
        short_url = await cls._generate_short_url()
        async with UrlRepository() as url_repository:
            url = await url_repository.create_url(
                short_url=short_url, full_url=full_url
            )
        return url

    @staticmethod
    async def get_url_by_short(short_url: str) -> entities.Url | None:
        async with UrlRepository() as url_repository:
            url = await url_repository.get_url_by_short(short_url=short_url)
        return url

    @staticmethod
    async def _generate_short_url() -> str:
        short_url_length = config.SHORT_URL_MIN_LENGTH
        tries_counter = 0
        async with UrlRepository() as url_repository:
            while True:
                short_url = RandomStringGenerator.get_random_string(
                    length=short_url_length
                )
                if not await url_repository.is_short_url_taken(short_url=short_url):
                    return short_url
                tries_counter += 1
                if tries_counter == 5:
                    short_url_length += 1
                    tries_counter = 0
