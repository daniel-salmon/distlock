import threading
from typing import TypedDict

from .exceptions import AlreadyExistsError
from .models import Lock


class Store(TypedDict):
    key: Lock


class LockStore:
    def __init__(self):
        self._store = Store()

    def __len__(self) -> int:
        return len(self._store)

    def __getitem__(self, key: str) -> Lock:
        return self._store[key]

    def __setitem__(self, key: str, value: Lock) -> None:
        self._store[key] = value

    def __delitem__(self, key: str) -> None:
        del self._store[key]

    def __contains__(self, key: str) -> bool:
        return key in self._store

    def acquire(self, key: str, expires_in_seconds: int) -> Lock:
        lock = self._store[key]
        if lock.acquired and not lock.expired:
            unacquired_lock = Lock(
                key=lock.key,
                acquired=False,
                clock=lock.clock,
                expires_at=lock.expires_at,
            )
            return unacquired_lock
        lock.acquire(expires_in_seconds=expires_in_seconds)
        return lock

    def release(self, key: str, clock: int) -> None:
        lock = self._store[key]
        lock.release(clock=clock)

    def set_not_exists(self, key: str, value: Lock) -> None:
        if key in self._store:
            raise AlreadyExistsError
        self._store[key] = value

    # We define this method so that the API of this class is the same as the
    # ThreadSafeLockStore class.
    def to_list(self) -> list[Lock]:
        return list(self._store.values())


class ThreadSafeLockStore:
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

    def acquire(self, key: str, expires_in_seconds: int) -> Lock:
        with self._lock:
            lock = self._store[key]
            if lock.acquired and not lock.expired:
                unacquired_lock = Lock(
                    key=lock.key,
                    acquired=False,
                    clock=lock.clock,
                    expires_at=lock.expires_at,
                )
                return unacquired_lock
            lock.acquire(expires_in_seconds=expires_in_seconds)
            return lock

    def release(self, key: str, clock: int) -> None:
        with self._lock:
            lock = self._store[key]
            lock.release(clock=clock)

    def set_not_exists(self, key: str, value: Lock) -> None:
        with self._lock:
            if key in self._store:
                raise AlreadyExistsError
            self._store[key] = value

    # Can't define __iter__ and use list(lock_store) in the
    # calling code because that would not be thread safe.
    def to_list(self) -> list[Lock]:
        with self._lock:
            return list(self._store.values())
