import threading
from datetime import datetime, timedelta, timezone
from typing import TypedDict

from .exceptions import AlreadyAcquiredError, AlreadyExistsError
from .models import Lock

TEN_MINUTES_IN_SECONDS = 10 * 60


class Store(TypedDict):
    key: Lock


class LockStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._store = Store()

    def __len__(self) -> int:
        with self._lock:
            return len(self._store)

    def __getitem__(self, key: str) -> Lock:
        with self._lock:
            return self._store[key]

    def __setitem__(self, key: str, value: Lock) -> None:
        with self._lock:
            self._store[key] = value

    def __delitem__(self, key: str) -> None:
        with self._lock:
            del self._store[key]

    def __contains__(self, key: str) -> bool:
        with self._lock:
            return key in self._store

    # Numeric scalars default to 0 on protobufs
    def acquire(self, key: str, timeout_seconds: int = 0) -> Lock:
        if timeout_seconds == 0:
            timeout_seconds = TEN_MINUTES_IN_SECONDS
        with self._lock:
            lock = self._store[key]
            if lock.acquired:
                raise AlreadyAcquiredError(
                    message=f"lock {key} already acquired by someone else",
                    timeout=lock.timeout,
                )
            lock.acquired = True
            lock.clock += 1
            lock.timeout = datetime.now(timezone.utc) + timedelta(
                seconds=timeout_seconds
            )
            return lock

    def set_not_exists(self, key: str, value: Lock) -> None:
        with self._lock:
            if key in self._store:
                raise AlreadyExistsError
            self._store[key] = value
