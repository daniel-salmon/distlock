import threading
from typing import TypedDict

from .exceptions import AlreadyExistsError
from .models import Lock


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

    def set_not_exists(self, key: str, value: Lock) -> None:
        with self._lock:
            if key in self._store:
                raise AlreadyExistsError
            self._store[key] = value
