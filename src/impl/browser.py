from asyncio import Lock

lock = Lock()


async def get(url: str, headers: dict[str, str]):
    from playwright.async_api import async_playwright

    async with lock, async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_extra_http_headers(headers)
        await page.goto(url)

        content = await page.evaluate("""
            async () => {
                const response = await fetch(location.href);
                const arrayBuffer = await response.arrayBuffer();
                return Array.from(new Uint8Array(arrayBuffer));
            }
        """)

        return bytes(content)
