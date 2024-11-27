from ..utils.cache import cache


@cache
def get_session():
    from curl_cffi.requests import AsyncSession

    return AsyncSession()


async def get(url: str, headers: dict):
    res = await get_session().get(url, headers=headers)
    res.raise_for_status()
    return res.content
