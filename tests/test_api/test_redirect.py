from unittest.mock import patch

from app.domain import entities


@patch("app.api.api.UrlService", autospec=True)
def test_redirect_not_existing_url(mocked_url_service, client):
    mocked_url_service.get_url_by_short.return_value = None
    short_url = "short_url"

    response = client.get(f"/{short_url}/")

    assert response.status_code == 404
    mocked_url_service.get_url_by_short.assert_awaited_once_with(short_url=short_url)


@patch("app.api.api.UrlService", autospec=True)
def test_redirect_existing_url(mocked_url_service, client):
    full_url = "http://full_url.com"
    short_url = "short_url"
    url = entities.Url(full_url=full_url, short_url=short_url)
    mocked_url_service.get_url_by_short.return_value = url

    response = client.get(f"/{short_url}/", allow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == full_url
    mocked_url_service.get_url_by_short.assert_awaited_once_with(short_url=short_url)
