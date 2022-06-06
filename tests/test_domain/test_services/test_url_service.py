from unittest.mock import patch, call

from app import config
from app.domain import entities
from app.domain.services.url_service import UrlService


@patch("app.domain.services.url_service.UrlRepository", autospec=True)
@patch("app.domain.services.url_service.UrlService._generate_short_url")
async def test_create_url_calls_repository_create_url(
    mocked_generate_short_url, mocked_url_repository
):
    full_url = "full_url"
    short_url = "short_url"
    mocked_url = entities.Url(
        short_url=short_url,
        full_url=full_url,
    )
    mocked_generate_short_url.return_value = short_url
    mocked_url_repository_instance = (
        mocked_url_repository.return_value.__aenter__.return_value
    )
    mocked_url_repository_instance.create_url.return_value = mocked_url

    url = await UrlService.create_url(full_url=full_url)

    assert url == mocked_url
    mocked_generate_short_url.assert_called_once()
    mocked_url_repository_instance.create_url.assert_awaited_once_with(
        short_url=short_url, full_url=full_url
    )


@patch("app.domain.services.url_service.UrlRepository", autospec=True)
async def test_get_url_by_short_calls_repository_get_url_by_short(
    mocked_url_repository,
):
    full_url = "full_url"
    short_url = "short_url"
    mocked_url = entities.Url(
        short_url=short_url,
        full_url=full_url,
    )
    mocked_url_repository_instance = (
        mocked_url_repository.return_value.__aenter__.return_value
    )
    mocked_url_repository_instance.get_url_by_short.return_value = mocked_url

    url = await UrlService.get_url_by_short(short_url=short_url)

    assert url == mocked_url
    mocked_url_repository_instance.get_url_by_short.assert_awaited_once_with(
        short_url=short_url
    )


@patch("app.domain.services.url_service.UrlRepository", autospec=True)
@patch("app.domain.services.url_service.RandomStringGenerator", autospec=True)
async def test_generate_short_url_tries_until_success(
    mocked_random_string_generator, mocked_url_repository
):
    mocked_url_repository_instance = (
        mocked_url_repository.return_value.__aenter__.return_value
    )
    # 5 times the proposed short url is already taken
    mocked_url_repository_instance.is_short_url_taken.side_effect = [True] * 5 + [False]
    random_strings = "abcdef"
    mocked_random_string_generator.get_random_string.side_effect = list(random_strings)

    short_url = await UrlService._generate_short_url()

    assert short_url == random_strings[5]
    mocked_random_string_generator.get_random_string.assert_has_calls(
        [call(length=config.SHORT_URL_MIN_LENGTH)] * 5
        + [call(length=config.SHORT_URL_MIN_LENGTH + 1)]
    )
    mocked_url_repository_instance.is_short_url_taken.assert_has_awaits(
        [call(short_url=short_url) for short_url in random_strings]
    )
