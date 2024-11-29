from contextlib import suppress
from urllib.parse import urljoin

from fastapi import Cookie, Depends, FastAPI, Header, Request, Response
from fastapi.responses import RedirectResponse
from pydantic_core import Url

from src.api import get
from src.utils.db import TypedDB

app = FastAPI()


filtered_headers = {"host", "origin", "cookie", "accept-encoding", "user-agent"}


def filter_headers(headers):
    return {key: value for key, value in headers.items() if key.lower() not in filtered_headers}


def get_filtered_headers(req: Request):
    return filter_headers(req.headers)


def get_url(url: Url):
    return str(url)


db = TypedDB[Response]("v1")


@app.get("/proxy")
async def proxy(url: str = Depends(get_url), headers=Depends(get_filtered_headers), accept: str = Header("", include_in_schema=False), refresh: bool = False):
    if not refresh:
        with suppress(KeyError):
            return db[url]
    content = await get(url, headers)
    res = Response(content)
    if "html" in accept:
        res.set_cookie("proxied_from", url)
    db[url] = res
    return res


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


@app.get("/{_:path}", include_in_schema=False)
async def other(_, req: Request, proxied_from: str = Cookie(), headers=Depends(get_filtered_headers), accept: str = Header("", include_in_schema=False)):
    url = urljoin(proxied_from, req.url.path)
    if req.url.query:
        url += f"?{req.url.query}"
    if req.url.fragment:
        url += f"#{req.url.fragment}"

    res = await get(url, headers)

    media_type = None

    # heuristics
    if url.endswith(".js"):
        media_type = "application/javascript"
    elif url.endswith(".css"):
        media_type = "text/css"
    elif url.endswith(".wasm"):
        media_type = "application/wasm"
    elif accept:
        for i in accept.split(","):
            if "*" not in i:
                media_type = i
                break
        else:
            if url.endswith(".json"):
                media_type = "application/json"
    return Response(res, media_type=media_type)


if not __debug__:
    from brotli_asgi import BrotliMiddleware
    from starlette.middleware.cors import CORSMiddleware
    from zstd_asgi import ZstdMiddleware

    app.add_middleware(CORSMiddleware, allow_origins="*", allow_headers="*")
    app.add_middleware(ZstdMiddleware, threads=-1, gzip_fallback=False)
    app.add_middleware(BrotliMiddleware)
