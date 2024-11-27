from ..utils.cache import cache


@cache
def get_session():
    from niquests import AsyncSession

    return AsyncSession()


async def get(url: str, headers: dict):
    res = await get_session().get(url, headers=headers)
    res.raise_for_status()
    assert res.content is not None
    return res.content
