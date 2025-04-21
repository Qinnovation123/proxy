from traceback import format_exception_only

from fastapi import HTTPException

from ..utils.ua import get_ua


class FetchError(HTTPException):
    def __init__(self):
        super().__init__(500, "Tried all fetch implementations, all failed.")


def get_error_message(e: Exception):
    return "\n".join(format_exception_only(e)).strip()


async def get(url: str, headers: dict):
    ua_headers = {"user-agent": get_ua()}
    headers["x-disclaimer"] = (
        "We are fetching this literature for academic research purposes only. "
        "We kindly request that you do not block our access. "
        "If you have any concerns, please contact me at Muspi Merol <me@promplate.dev>. "
        "Thank you for your understanding."
    )

    from ..impl.niquests import get

    try:
        return await get(url, headers | ua_headers)
    except Exception as e:
        print("niquests: ", get_error_message(e))

    from ..impl.httpx import get

    try:
        return await get(url, headers | ua_headers)
    except Exception as e:
        print("httpx: ", get_error_message(e))

    from ..impl.curl import get

    try:
        return await get(url, headers | ua_headers)
    except Exception as e:
        print("curl: ", get_error_message(e))

    from ..impl.browser import get

    try:
        return await get(url, headers)
    except Exception as e:
        print("browser: ", get_error_message(e))

    raise FetchError
