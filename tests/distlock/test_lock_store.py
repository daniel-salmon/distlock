import pytest

from distlock.exceptions import AlreadyExistsError
from distlock.lock_store import ThreadSafeLockStore
from distlock.models import Lock

keys = ["a_lock", "another_lock", "pizza"]


def test_lock_store_init() -> None:
    lock_store = ThreadSafeLockStore()
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_lock_store_set_get_del(key: str) -> None:
    lock_store = ThreadSafeLockStore()
    lock = Lock()
    lock_store[key] = lock
    assert key in lock_store
    assert lock_store[key] == lock
    del lock_store[key]
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_lock_store_set_not_exists(key: str) -> None:
    lock_store = ThreadSafeLockStore()
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
