from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from pydantic_core import Url

app = FastAPI()


filtered_headers = {"host", "origin", "cookie", "accept-encoding", "user-agent"}


@app.get("/proxy", response_class=Response)
async def get(url: Url, req: Request):
    from src.api import FetchError, get

    try:
        return await get(str(url), headers={key: value for key, value in req.headers.items() if key.lower() not in filtered_headers})
    except FetchError as e:
        raise HTTPException(500, str(e)) from e


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")


if not __debug__:
    from brotli_asgi import BrotliMiddleware
    from starlette.middleware.cors import CORSMiddleware
    from zstd_asgi import ZstdMiddleware

    app.add_middleware(CORSMiddleware, allow_origins="*", allow_headers="*")
    app.add_middleware(ZstdMiddleware, threads=-1, gzip_fallback=False)
    app.add_middleware(BrotliMiddleware)
