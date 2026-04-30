import time
from threading import Lock

# Simple in-memory TTL cache for per-worker caching.
# Not shared across processes (gunicorn workers) — useful as a quick, low-effort speedup.
_CACHE = {}
_LOCK = Lock()


def cache_set(key: str, value, ttl: int = 60):
    """Store value under key for ttl seconds."""
    expire_at = time.time() + int(ttl)
    with _LOCK:
        _CACHE[key] = (value, expire_at)


def cache_get(key: str):
    """Return cached value or None if missing/expired."""
    with _LOCK:
        entry = _CACHE.get(key)
        if not entry:
            return None
        value, expire_at = entry
        if time.time() > expire_at:
            del _CACHE[key]
            return None
        return value


def cache_delete(key: str):
    with _LOCK:
        _CACHE.pop(key, None)
