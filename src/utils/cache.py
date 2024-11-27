from asyncio import ensure_future, iscoroutine
from collections.abc import Callable
from functools import wraps


def cache[**P, T](func: Callable[P, T]) -> Callable[P, T]:
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        assert not kwargs, kwargs  # kwargs are not supported

        if args not in cache:
            value = func(*args, **kwargs)
            if iscoroutine(value):
                value = ensure_future(value)
            cache[args] = value
        else:
            value = cache[args]

        return value  # type: ignore

    return wrapper
