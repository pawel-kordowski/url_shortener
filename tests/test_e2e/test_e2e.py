def test_create_and_retrieve_url(client, setup_database):
    full_url = "http://google.com"

    create_response = client.post("/urls/", json={"url": full_url})

    assert create_response.status_code == 201
    short_url = create_response.json()["short_url"]
    assert short_url != full_url

    retrieve_response = client.get(short_url, allow_redirects=False)

    assert retrieve_response.status_code == 307
    assert retrieve_response.headers["location"] == full_url
