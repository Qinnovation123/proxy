from __future__ import annotations

from typing import TYPE_CHECKING

from ..utils.cache import cache

if TYPE_CHECKING:
    from playwright.async_api import Request, Route


async def handle_route(route: Route, _: Request):
    res = await route.fetch()
    res.headers.update(
        {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )
    await route.fulfill(response=res)


@cache
async def get_context():
    from playwright.async_api import async_playwright

    playwright = await async_playwright().start()

    browser = await playwright.chromium.launch()
    context = await browser.new_context()
    await context.route("**/*", handle_route)
    return context


async def get(url: str, headers: dict[str, str]):
    context = await get_context()
    async with await context.new_page() as page:
        await page.set_extra_http_headers(headers)
        content = await page.evaluate(f"""
            async () => {{
                const response = await fetch({url!r});
                if (!response.ok) throw new Error(response.statusText);
                const arrayBuffer = await response.arrayBuffer();
                return Array.from(new Uint8Array(arrayBuffer));
            }}
        """)

        return bytes(content)
