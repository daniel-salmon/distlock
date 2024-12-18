from threading import Lock

import pytest

from distlock.lock_store import AlreadyExistsError, LockStore

keys = ["a_lock", "another_lock", "pizza"]


def test_lock_store_init() -> None:
    lock_store = LockStore()
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_lock_store_set_get_del(key: str) -> None:
    lock_store = LockStore()
    lock = Lock()
    lock_store[key] = lock
    assert key in lock_store
    assert lock_store[key] == lock
    del lock_store[key]
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_lock_store_set_not_exists(key: str) -> None:
    lock_store = LockStore()
    lock = Lock()
    lock_store.set_not_exists(key, lock)
    assert key in lock_store
    assert lock_store[key] == lock
    with pytest.raises(AlreadyExistsError):
        lock_store.set_not_exists(key, lock)
    del lock_store[key]
    lock_store.set_not_exists(key, lock)
    assert key in lock_store
    assert lock_store[key] == lock
