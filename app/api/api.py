from fastapi import FastAPI, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import RedirectResponse

from app.api.models import UrlInput, UrlOutput
from app.domain.services.url_service import UrlService

app = FastAPI()


@app.get("/{short_url}/")
async def redirect(short_url: str):
    url = await UrlService.get_url_by_short(short_url=short_url)
    if url is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return RedirectResponse(url.full_url)


@app.post("/urls/", status_code=status.HTTP_201_CREATED, response_model=UrlOutput)
async def create_url(url: UrlInput, request: Request) -> UrlOutput:
    created_url = await UrlService.create_url(full_url=url.url)
    short_url = request.url_for("redirect", short_url=created_url.short_url)
    return UrlOutput(full_url=created_url.full_url, short_url=short_url)
