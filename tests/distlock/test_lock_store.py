import pytest

from distlock.exceptions import AlreadyExistsError
from distlock.lock_store import LockStore
from distlock.models import Mutex

keys = ["a_lock", "another_lock", "pizza"]


def test_lock_store_init() -> None:
    lock_store = LockStore()
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_lock_store_set_get_del(key: str) -> None:
    lock_store = LockStore()
    mutex = Mutex()
    lock_store[key] = mutex
    assert key in lock_store
    assert lock_store[key] == mutex
    del lock_store[key]
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_lock_store_set_not_exists(key: str) -> None:
    lock_store = LockStore()
    mutex = Mutex()
    lock_store.set_not_exists(key, mutex)
    assert key in lock_store
    assert lock_store[key] == mutex
    with pytest.raises(AlreadyExistsError):
        lock_store.set_not_exists(key, mutex)
    del lock_store[key]
    lock_store.set_not_exists(key, mutex)
    assert key in lock_store
    assert lock_store[key] == mutex
