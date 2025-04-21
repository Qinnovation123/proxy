from pathlib import Path
from typing import Unpack

from diskcache import Cache as BaseCache
from diskcache.core import Settings

cache_root = Path(__file__, "../../../cache").resolve()


class Cache[V](BaseCache[str, V]):
    def __init__(self, directory: str, **settings: Unpack[Settings]):
        path = cache_root / directory
        path.mkdir(parents=True, exist_ok=True)
        super().__init__(path, **settings)
