from pathlib import Path

from diskcache import Cache as BaseCache

cache_root = Path(__file__, "../../../cache").resolve()


class Cache[V](BaseCache[str, V]):
    def __init__(self, directory: str):
        path = cache_root / directory
        path.mkdir(parents=True, exist_ok=True)
        super().__init__(path)
