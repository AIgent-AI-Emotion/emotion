from threading import RLock
from typing import Dict, Any, List
import copy
import time


class MemoryStore:
    """
    Simple thread-safe in-memory store.
    NOTE: This is ephemeral in serverless environments (Vercel cold starts).
    Replace with a persistent backend (Postgres/Redis) for production.
    """

    def __init__(self):
        self._lock = RLock()
        self._data: Dict[str, Any] = {
            "kwords": [],     # list[dict]
            "metrics": {},    # dict[str, Any]
            "snapshots": []   # list[dict]
        }

    def get(self, key: str, default=None):
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any):
        with self._lock:
            self._data[key] = value

    def append(self, key: str, value: Any):
        with self._lock:
            lst: List[Any] = self._data.setdefault(key, [])
            lst.append(value)
            return value

    def all(self) -> Dict[str, Any]:
        """Return a deep-copied snapshot to avoid external mutation."""
        with self._lock:
            return copy.deepcopy(self._data)

    def now(self) -> float:
        return time.time()


# Global singleton store
STORE = MemoryStore()
