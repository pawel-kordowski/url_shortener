from sqlalchemy import select

from app.database import engine
from app.domain import entities
from app.domain.repositories.url_repository import UrlRepository
from app.models.url import Url
from tests.test_repositories.sqlalchemy_helpers import QueryCounter


async def test_get_url_by_short_returns_none_when_no_match(db_session):
    async with UrlRepository() as url_repository:
        with QueryCounter(engine.sync_engine) as query_counter:
            url = await url_repository.get_url_by_short(short_url="not_matching")

    assert url is None
    assert query_counter.count == 1


async def test_get_url_by_short_returns_url_when_match(db_session):
    url = Url(full_url="full_url", short_url="short_url")
    db_session.add(url)
    await db_session.commit()

    async with UrlRepository() as url_repository:
        with QueryCounter(engine.sync_engine) as query_counter:
            url = await url_repository.get_url_by_short(short_url=url.short_url)

    assert url == entities.Url(short_url=url.short_url, full_url=url.full_url)
    assert query_counter.count == 1


async def test_create_url(db_session):
    full_url = "full_url"
    short_url = "short_url"

    async with UrlRepository() as url_repository:
        with QueryCounter(engine.sync_engine) as query_counter:
            url = await url_repository.create_url(
                short_url=short_url, full_url=full_url
            )

    assert url == entities.Url(full_url=full_url, short_url=short_url)
    assert query_counter.count == 1

    all_urls_query = select(Url)
    results = (await db_session.execute(all_urls_query)).all()

    assert len(results) == 1
    created_url = results[0][0]
    assert created_url.full_url == full_url
    assert created_url.short_url == short_url


async def test_is_short_url_taken_not_taken_case(db_session):
    async with UrlRepository() as url_repository:
        with QueryCounter(engine.sync_engine) as query_counter:
            taken = await url_repository.is_short_url_taken(short_url="not_taken")

    assert taken is False
    assert query_counter.count == 1


async def test_is_short_url_taken_taken_case(db_session):
    url = Url(full_url="full_url", short_url="short_url")
    db_session.add(url)
    await db_session.commit()

    async with UrlRepository() as url_repository:
        with QueryCounter(engine.sync_engine) as query_counter:
            taken = await url_repository.is_short_url_taken(short_url=url.short_url)

    assert taken is True
    assert query_counter.count == 1
