import asyncio
import time

import pytest

from distlock import (
    AlreadyExistsError,
    DistlockAsync,
    Lock,
    NotFoundError,
)
from distlock.exceptions import UnreleasableError

from .conftest import cleanup_async


@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["key", "different key", "one more key"])
async def test_create_lock_async(key: str, distlock_async: DistlockAsync) -> None:
    await distlock_async.create_lock(key)
    await cleanup_async(distlock_async, keys=[key])


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "keys",
    [
        ["key1", "key2", "key3"],
        ["value1", "value2", "value3"],
    ],
)
async def test_create_locks_async(
    keys: list[str], distlock_async: DistlockAsync
) -> None:
    for key in keys:
        await distlock_async.create_lock(key)
    locks = await distlock_async.list_locks()
    lock_keys = {lock.key for lock in locks}
    assert all(key in lock_keys for key in keys)
    await cleanup_async(distlock_async, keys=keys)


@pytest.mark.asyncio
async def test_create_lock_that_exists_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        with pytest.raises(AlreadyExistsError):
            await distlock_async.create_lock(key)


@pytest.mark.asyncio
async def test_get_lock_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        lock = await distlock_async.get_lock(key)
        assert lock.key == key


@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
async def test_get_lock_that_does_not_exist_async(
    key: str, create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        _ = await distlock_async.get_lock(key)


@pytest.mark.asyncio
async def test_list_locks_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    locks = await distlock_async.list_locks()
    all_keys = {lock.key for lock in locks}
    assert all(key in all_keys for key in create_locks)


@pytest.mark.asyncio
async def test_delete_locks_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        await distlock_async.delete_lock(key)
        with pytest.raises(NotFoundError):
            await distlock_async.get_lock(key)


@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
async def test_delete_lock_that_does_not_exist_async(
    key: str, create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        await distlock_async.delete_lock(key)


@pytest.mark.asyncio
async def test_acquire_locks_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    locks = await asyncio.gather(
        *[
            distlock_async.acquire_lock(key, expires_in_seconds=1)
            for key in create_locks
        ]
    )
    assert all(lock.acquired for lock in locks)


@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
async def test_acquire_lock_that_does_not_exist_async(
    key: str, create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        _ = await distlock_async.acquire_lock(key, expires_in_seconds=1)


@pytest.mark.asyncio
async def test_acquire_and_release_locks_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    locks = await asyncio.gather(
        *[
            distlock_async.acquire_lock(key, expires_in_seconds=1)
            for key in create_locks
        ]
    )
    assert all(lock.acquired for lock in locks)
    for lock in locks:
        await distlock_async.release_lock(lock)
    locks = await asyncio.gather(
        *[distlock_async.get_lock(key) for key in create_locks]
    )
    assert all(not lock.acquired for lock in locks)


@pytest.mark.asyncio
@pytest.mark.parametrize("key", ["not-a-key-1", "not-a-key-2", "not-a-key-3"])
async def test_release_lock_that_does_not_exist_async(
    key: str, create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    assert key not in create_locks
    with pytest.raises(NotFoundError):
        await distlock_async.release_lock(Lock(key=key))


@pytest.mark.asyncio
async def test_release_lock_out_of_sync_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    """
    This simulates a case where a client attempts to release a lock that,
    according to the server, the client may no longer hold, since the client's
    clock for the lock is out of sync. The client should be made aware that the
    lock they just attempted to release could not be released because they
    did not hold the lock.
    """
    locks = await asyncio.gather(
        *[distlock_async.get_lock(key) for key in create_locks]
    )
    assert all(lock.clock == 0 for lock in locks)
    for lock in locks:
        lock.clock += 1
        with pytest.raises(UnreleasableError):
            await distlock_async.release_lock(lock)
        lock.clock -= 1

    # Now actually acquire the locks, bumping up their server-side clocks
    # And then attempting release with a clock value lower than that
    # on the server
    for lock in locks:
        await distlock_async.acquire_lock(key=lock.key, expires_in_seconds=20)
        updated_lock = await distlock_async.get_lock(lock.key)
        assert updated_lock.acquired
        assert updated_lock.clock == 1
        updated_lock.clock -= 1
        with pytest.raises(UnreleasableError):
            await distlock_async.release_lock(updated_lock)


@pytest.mark.asyncio
async def test_acquire_lock_no_blocking_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        await distlock_async.acquire_lock(key, expires_in_seconds=60)
        lock = await distlock_async.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        start = time.time()
        unacquired_lock = await distlock_async.acquire_lock(
            key=key,
            expires_in_seconds=60,
            blocking=False,
        )
        elapsed = time.time() - start
        assert not unacquired_lock.acquired
        assert elapsed < 1.0


@pytest.mark.asyncio
async def test_acquire_lock_blocking_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        await distlock_async.acquire_lock(key, expires_in_seconds=3)
        lock = await distlock_async.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        start = time.time()
        acquired_lock = await distlock_async.acquire_lock(
            key=key,
            expires_in_seconds=3,
            blocking=True,
        )
        elapsed = time.time() - start
        assert acquired_lock.acquired
        assert acquired_lock.clock == 2
        assert elapsed > 2.0


@pytest.mark.asyncio
async def test_acquire_lock_blocking_heartbeats_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        await distlock_async.acquire_lock(key, expires_in_seconds=5)
        lock = await distlock_async.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        start = time.time()
        acquired_lock = await distlock_async.acquire_lock(
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


@pytest.mark.asyncio
async def test_acquire_lock_blocking_timeout_async(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    for key in create_locks:
        await distlock_async.acquire_lock(key, expires_in_seconds=3)
        lock = await distlock_async.get_lock(key)
        assert lock.acquired
        assert lock.clock == 1
        with pytest.raises(TimeoutError):
            _ = await distlock_async.acquire_lock(
                key=key,
                expires_in_seconds=3,
                blocking=True,
                timeout_seconds=0.1,
            )


@pytest.mark.asyncio
async def test_acquire_release_cycle_clock_updates(
    create_locks: list[str], distlock_async: DistlockAsync
) -> None:
    locks = await asyncio.gather(
        *[
            distlock_async.acquire_lock(key, expires_in_seconds=3)
            for key in create_locks
        ]
    )
    assert all(lock.acquired for lock in locks)
    assert all(lock.clock == 1 for lock in locks)
    for lock in locks:
        await distlock_async.release_lock(lock)
    locks = await asyncio.gather(
        *[distlock_async.get_lock(key) for key in create_locks]
    )
    assert all(not lock.acquired for lock in locks)
    assert all(lock.clock == 1 for lock in locks)
    locks = await asyncio.gather(
        *[
            distlock_async.acquire_lock(key, expires_in_seconds=3)
            for key in create_locks
        ]
    )
    assert all(lock.acquired for lock in locks)
    assert all(lock.clock == 2 for lock in locks)
    for lock in locks:
        await distlock_async.release_lock(lock)
    locks = await asyncio.gather(
        *[distlock_async.get_lock(key) for key in create_locks]
    )
    assert all(not lock.acquired for lock in locks)
    assert all(lock.clock == 2 for lock in locks)
