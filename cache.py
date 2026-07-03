import time
from typing import Any, Optional


class InMemoryCache:
    """Простой in-memory кэш с TTL (time-to-live)."""

    def __init__(self):
        self._cache: dict[str, dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None
        entry = self._cache[key]
        if time.time() > entry["expires_at"]:
            del self._cache[key]
            return None
        return entry["value"]

    def set(self, key: str, value: Any, ttl: int = 60) -> None:
        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
        }

    def clear(self) -> None:
        self._cache.clear()


cache = InMemoryCache()