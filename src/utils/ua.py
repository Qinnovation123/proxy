from fake_useragent import FakeUserAgent

ua = FakeUserAgent()


def get_ua() -> str:
    return ua.random
