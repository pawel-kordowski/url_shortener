# url shortener
A small project to create and retrieve short form of long urls.

### how to run app locally
```shell
cp .env.example .env
make up
```

### how to run tests locally
```shell
cp .env.example .env
make test
```

### example HTTP requests
* create url via POST to `/urls/`
```shell
$ curl --request POST 'http://localhost:8000/urls/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "url": "http://google.com"
}'

{"full_url":"http://google.com","short_url":"http://localhost:8000/dHHVv/"}
```
* retrieve url (get redirect) via GET to `/{url}/`
```shell
$ curl 'http://localhost:8000/dHHVv/' -v
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8000 (#0)
> GET /dHHVv/ HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/7.58.0
> Accept: */*
> 
< HTTP/1.1 307 Temporary Redirect
< date: Mon, 06 Jun 2022 18:11:57 GMT
< server: uvicorn
< content-length: 0
< location: http://google.com
< 
* Connection #0 to host localhost left intact
```

### tech stack
* PostgreSQL as a database
* async FastAPI as a web framework
* uvicorn as a web server
* async SQLAlchemy as an ORM
* alembic to manage database migrations
* pytest for unit tests
* poetry to manage python packages
* docker and docker-compose to create local environment
* black, flake8 and isort to keep code quality

### architecture
Architecture is inspired by the [hexagonal architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)).
All the logic used by API endpoints is kept in `UrlService`. The service class
uses `UrlRepository` to connect to database. Only the pure data classes called here 
entities are crossing the boundaries.