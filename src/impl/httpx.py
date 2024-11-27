from ..utils.cache import cache


@cache
def get_client():
    from httpx import AsyncClient

    return AsyncClient(http2=True, follow_redirects=True)


async def get(url: str, headers: dict):
    from httpx import AsyncClient

    async with AsyncClient(http2=True, headers=headers, follow_redirects=True) as client:
        res = await client.get(url)
        return res.raise_for_status().content
