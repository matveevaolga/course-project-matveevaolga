from datetime import datetime, timedelta
from typing import Any, Optional


class SimpleCache:
    def __init__(self):
        self._cache = {}

    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            data, expiry = self._cache[key]
            if datetime.now() < expiry:
                return data
            else:
                del self._cache[key]
        return None

    def set(self, key: str, value: Any, ttl_seconds: int = 30) -> None:
        expiry = datetime.now() + timedelta(seconds=ttl_seconds)
        self._cache[key] = (value, expiry)

    def invalidate(self, key: str) -> None:
        if key in self._cache:
            del self._cache[key]

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> dict:
        total_entries = len(self._cache)
        valid_entries = 0
        now = datetime.now()
        for key in list(self._cache.keys()):
            data, expiry = self._cache[key]
            if now < expiry:
                valid_entries += 1
            else:
                del self._cache[key]
        return {
            "total_entries": total_entries,
            "valid_entries": valid_entries,
            "hit_ratio": "N/A",
        }


cache = SimpleCache()
