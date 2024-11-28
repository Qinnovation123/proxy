from pathlib import Path

cache_root = Path(__file__, "../../../cache").resolve()


class TypedDB[T]:
    def __init__(self, name: str):
        from diskcache import Cache

        path = cache_root / name
        path.mkdir(parents=True, exist_ok=True)

        self.cache = Cache(path)

    def __getitem__(self, key: str) -> T:
        return self.cache[key]  # type: ignore

    def __setitem__(self, key: str, value: T):
        self.cache[key] = value
