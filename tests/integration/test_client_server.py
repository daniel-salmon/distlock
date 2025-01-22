import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

import pytest

from distlock import (
    AlreadyExistsError,
    Distlock,
    Lock,
    NotFoundError,
    UnreleasableError,
)

from .conftest import cleanup


@pytest.mark.parametrize("key", ["key", "different key", "one more key"])
def test_create_lock(key: str, distlock: Distlock) -> None:
    distlock.create_lock(key)
    cleanup(distlock, keys=[key])


@pytest.mark.parametrize(
    "keys",
    [
        ["key1", "key2", "key3"],
        ["value1", "value2", "value3"],
    ],
)
def test_create_locks(keys: list[str], distlock: Distlock) -> None:
    for key in keys:
        distlock.create_lock(key)
    lock_keys = {lock.key for lock in distlock.list_locks()}
    assert all(key in lock_keys for key in keys)
    cleanup(distlock, keys=keys)


def test_create_lock_that_exists(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        with pytest.raises(AlreadyExistsError):
            distlock.create_lock(key)


def test_get_lock(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        lock = distlock.get_lock(key)
        assert lock.key == key


@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
def test_get_lock_that_does_not_exist(
    key: str, create_locks: list[str], distlock: Distlock
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        _ = distlock.get_lock(key)


def test_list_locks(create_locks: list[str], distlock: Distlock) -> None:
    all_keys = {lock.key for lock in distlock.list_locks()}
    assert all(key in all_keys for key in create_locks)


def test_delete_locks(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        distlock.delete_lock(key)
        with pytest.raises(NotFoundError):
            distlock.get_lock(key)


@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
def test_delete_lock_that_does_not_exist(
    key: str, create_locks: list[str], distlock: Distlock
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        distlock.delete_lock(key)


def test_acquire_locks(create_locks: list[str], distlock: Distlock) -> None:
    locks = [
        distlock.acquire_lock(key=key, expires_in_seconds=1) for key in create_locks
    ]
    assert all(lock.acquired for lock in locks)


@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
def test_acquire_lock_that_does_not_exist(
    key: str, create_locks: list[str], distlock: Distlock
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        _ = distlock.acquire_lock(key=key, expires_in_seconds=1)


def test_acquire_and_release_locks(create_locks: list[str], distlock: Distlock) -> None:
    locks = [
        distlock.acquire_lock(key=key, expires_in_seconds=1) for key in create_locks
    ]
    assert all(lock.acquired for lock in locks)
    for lock in locks:
        distlock.release_lock(lock)
    locks = [distlock.get_lock(key) for key in create_locks]
    assert all(not lock.acquired for lock in locks)


@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
def test_release_lock_that_does_not_exist(
    key: str, create_locks: list[str], distlock: Distlock
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        distlock.release_lock(Lock(key=key))


def test_release_lock_out_of_sync(create_locks: list[str], distlock: Distlock) -> None:
    """
    This simulates a case where a client attempts to release a lock that,
    according to the server, the client may no longer hold, since the client's
    clock for the lock is out of sync. The client should be made aware that the
    lock they just attempted to release could not be released because they
    did not hold the lock.
    """
    locks = [distlock.get_lock(key) for key in create_locks]
    assert all(lock.clock == 0 for lock in locks)
    for lock in locks:
        lock.clock += 1
        with pytest.raises(UnreleasableError):
            distlock.release_lock(lock)
        lock.clock -= 1

    # Now actually acquire the locks, bumping up their server-side clocks
    # And then attempting release with a clock value lower than that
    # on the server
    for lock in locks:
        distlock.acquire_lock(key=lock.key, expires_in_seconds=20)
        updated_lock = distlock.get_lock(lock.key)
        assert updated_lock.acquired
        assert updated_lock.clock == 1
        updated_lock.clock -= 1
        with pytest.raises(UnreleasableError):
            distlock.release_lock(updated_lock)


def test_acquire_lock_no_blocking(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        distlock.acquire_lock(key=key, expires_in_seconds=60)
        lock = distlock.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        start = time.time()
        unacquired_lock = distlock.acquire_lock(
            key=key,
            expires_in_seconds=60,
            blocking=False,
        )
        elapsed = time.time() - start
        assert not unacquired_lock.acquired
        assert elapsed < 1.0


def test_acquire_lock_blocking(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        distlock.acquire_lock(key=key, expires_in_seconds=3)
        lock = distlock.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        start = time.time()
        acquired_lock = distlock.acquire_lock(
            key=key,
            expires_in_seconds=3,
            blocking=True,
        )
        elapsed = time.time() - start
        assert acquired_lock.acquired
        assert acquired_lock.clock == 2
        assert elapsed > 2.0


def test_acquire_lock_blocking_heartbeats(
    create_locks: list[str], distlock: Distlock
) -> None:
    for key in create_locks:
        distlock.acquire_lock(key=key, expires_in_seconds=5)
        lock = distlock.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        start = time.time()
        acquired_lock = distlock.acquire_lock(
            key=key,
            expires_in_seconds=5,
            blocking=True,
            timeout_seconds=10,
            heartbeat_seconds=1,
        )
        elapsed = time.time() - start
        assert acquired_lock.acquired
        assert acquired_lock.clock == 2
        assert elapsed > 4.0


def test_acquire_lock_blocking_timeout(
    create_locks: list[str], distlock: Distlock
) -> None:
    for key in create_locks:
        distlock.acquire_lock(key=key, expires_in_seconds=3)
        lock = distlock.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        with pytest.raises(TimeoutError):
            _ = distlock.acquire_lock(
                key=key,
                expires_in_seconds=3,
                blocking=True,
                timeout_seconds=0.1,
            )


def test_acquire_release_cycle_clock_updates(
    create_locks: list[str], distlock: Distlock
) -> None:
    locks = [
        distlock.acquire_lock(key=key, expires_in_seconds=3) for key in create_locks
    ]
    assert all(lock.acquired for lock in locks)
    assert all(lock.clock == 1 for lock in locks)
    for lock in locks:
        distlock.release_lock(lock)
    locks = [distlock.get_lock(key) for key in create_locks]
    assert all(not lock.acquired for lock in locks)
    assert all(lock.clock == 1 for lock in locks)
    locks = [
        distlock.acquire_lock(key=key, expires_in_seconds=3) for key in create_locks
    ]
    assert all(lock.acquired for lock in locks)
    assert all(lock.clock == 2 for lock in locks)
    for lock in locks:
        distlock.release_lock(lock)
    locks = [distlock.get_lock(key) for key in create_locks]
    assert all(not lock.acquired for lock in locks)
    assert all(lock.clock == 2 for lock in locks)


def test_multiple_clients(distlock_server: subprocess.Popen) -> None:
    def client(key: str) -> None:
        distlock = Distlock()
        distlock.create_lock(key)
        lock = distlock.get_lock(key)
        assert not lock.acquired
        assert lock.clock == 0
        lock = distlock.acquire_lock(key=key, expires_in_seconds=1)
        assert lock.acquired
        assert lock.clock == 1
        distlock.release_lock(lock)
        lock = distlock.get_lock(key)
        assert not lock.acquired
        assert lock.clock == 1
        distlock.delete_lock(key)
        with pytest.raises(NotFoundError):
            distlock.get_lock(key)

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(client, ["key1", "key2", "key3"])
    _ = [result for result in results]
