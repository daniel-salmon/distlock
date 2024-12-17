from threading import Lock
from typing import TypedDict


class Locks(TypedDict):
    key: Lock


class LockStore:
    def __init__(self):
        self.lock = Lock()
        self.locks = Locks()

    def __len__(self) -> int:
        with self.lock:
            return len(self.locks)

    def __getitem__(self, key: str) -> Lock:
        with self.lock:
            return self.locks[key]

    def __setitem__(self, key: str, value: Lock) -> None:
        with self.lock:
            self.locks[key] = value

    def __delitem__(self, key: str) -> None:
        with self.lock:
            del self.locks[key]

    def __contains__(self, key: str) -> bool:
        with self.lock:
            return key in self.locks
