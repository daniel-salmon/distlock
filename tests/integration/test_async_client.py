import asyncio

import pytest

from distlock import (
    AlreadyExistsError,
    DistlockAsync,
    NotFoundError,
)

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
