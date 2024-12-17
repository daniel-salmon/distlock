from threading import Lock

import pytest

from distlock.lock_store import LockStore


def test_lock_store_init() -> None:
    lock_store = LockStore()
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", ["a_lock", "another_lock", "pizza"])
def test_lock_store_set_get_del(key: str) -> None:
    lock_store = LockStore()
    lock = Lock()
    lock_store[key] = lock
    assert key in lock_store
    assert lock_store[key] == lock
    del lock_store[key]
    assert len(lock_store) == 0
