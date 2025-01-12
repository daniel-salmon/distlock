import pytest

from distlock import Distlock, UnreleasableError

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
    cleanup(distlock, keys=keys)


def test_get_lock(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        lock = distlock.get_lock(key)
        assert lock.key == key


def test_list_locks(create_locks: list[str], distlock: Distlock) -> None:
    all_keys = {lock.key for lock in distlock.list_locks()}
    assert all(key in all_keys for key in create_locks)


def test_delete_locks(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        distlock.delete_lock(key)


def test_acquire_locks(create_locks: list[str], distlock: Distlock) -> None:
    locks = [distlock.acquire_lock(key, expires_in_seconds=1) for key in create_locks]
    assert all(lock.acquired for lock in locks)


def test_acquire_and_release_locks(create_locks: list[str], distlock: Distlock) -> None:
    locks = [distlock.acquire_lock(key, expires_in_seconds=1) for key in create_locks]
    assert all(lock.acquired for lock in locks)
    for lock in locks:
        distlock.release_lock(lock)
    locks = [distlock.get_lock(key) for key in create_locks]
    assert all(not lock.acquired for lock in locks)


# This simulates a case where a client attempts to release a lock that,
# according to the server, the client may no longer hold, since the client's
# clock for the lock is out of sync. The client should be made aware that the
# lock they just attempted to release could not be released because they
# did not hold the lock.
def test_bad_release(create_locks: list[str], distlock: Distlock) -> None:
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
