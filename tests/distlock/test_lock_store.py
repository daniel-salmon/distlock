import pytest

from distlock.exceptions import AlreadyExistsError
from distlock.lock_store import LockStore, ThreadSafeLockStore
from distlock.models import Lock

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


@pytest.mark.parametrize("key", keys)
def test_lock_store_acquire_release(key: str) -> None:
    lock_store = LockStore()
    lock_store[key] = Lock(key=key)

    # Test acquiring an available lock
    acquired_lock = lock_store.acquire(key, expires_in_seconds=60)
    assert acquired_lock.acquired
    assert not acquired_lock.expired

    # Test acquiring an already acquired lock
    unacquired_lock = lock_store.acquire(key, expires_in_seconds=60)
    assert not unacquired_lock.acquired

    # Test releasing a lock
    lock_store.release(key, clock=1)
    released_lock = lock_store[key]
    assert not released_lock.acquired


@pytest.mark.parametrize("keys", [[], ["key"], keys])
def test_lock_store_to_list(keys: str) -> None:
    lock_store = LockStore()
    locks = [Lock(key=key) for key in sorted(keys)]
    for lock in locks:
        lock_store[lock.key] = lock
    stored_locks = lock_store.to_list()
    assert sorted(stored_locks, key=lambda lock: lock.key) == locks


def test_thread_safe_lock_store_init() -> None:
    lock_store = ThreadSafeLockStore()
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_thread_safe_lock_store_set_get_del(key: str) -> None:
    lock_store = ThreadSafeLockStore()
    lock = Lock()
    lock_store[key] = lock
    assert key in lock_store
    assert lock_store[key] == lock
    del lock_store[key]
    assert len(lock_store) == 0


@pytest.mark.parametrize("key", keys)
def test_thread_safe_lock_store_set_not_exists(key: str) -> None:
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


@pytest.mark.parametrize("key", keys)
def test_thread_safe_lock_store_acquire_release(key: str) -> None:
    lock_store = LockStore()
    lock_store[key] = Lock(key=key)

    # Test acquiring an available lock
    acquired_lock = lock_store.acquire(key, expires_in_seconds=60)
    assert acquired_lock.acquired
    assert not acquired_lock.expired

    # Test acquiring an already acquired lock
    unacquired_lock = lock_store.acquire(key, expires_in_seconds=60)
    assert not unacquired_lock.acquired

    # Test releasing a lock
    lock_store.release(key, clock=1)
    released_lock = lock_store[key]
    assert not released_lock.acquired


@pytest.mark.parametrize("keys", [[], ["key"], keys])
def test_thread_safe_lock_store_to_list(keys: str) -> None:
    lock_store = ThreadSafeLockStore()
    locks = [Lock(key=key) for key in sorted(keys)]
    for lock in locks:
        lock_store[lock.key] = lock
    stored_locks = lock_store.to_list()
    assert sorted(stored_locks, key=lambda lock: lock.key) == locks
