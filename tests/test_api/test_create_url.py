from unittest.mock import patch

from app.domain import entities


@patch("app.api.api.UrlService", autospec=True)
def test_create_url_invalid_url(mocked_url_service, client):
    response = client.post("/urls/", json={"url": "full_url"})

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"loc": ["body", "url"], "msg": "Invalid URL", "type": "value_error"}
        ]
    }
    mocked_url_service.create_url.assert_not_awaited()


@patch("app.api.api.UrlService", autospec=True)
def test_create_url(mocked_url_service, client):
    full_url = "http://full-url.com"
    short_url = "short_url"
    url = entities.Url(full_url=full_url, short_url=short_url)
    mocked_url_service.create_url.return_value = url

    response = client.post("/urls/", json={"url": full_url})

    assert response.status_code == 201
    assert response.json() == {
        "full_url": full_url,
        "short_url": f"http://testserver/{short_url}/",
    }
    mocked_url_service.create_url.assert_awaited_once_with(full_url=full_url)
