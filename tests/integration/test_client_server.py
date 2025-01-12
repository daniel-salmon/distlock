import pytest

from distlock import Distlock

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


def test_delete_locks(create_locks: list[str], distlock: Distlock) -> None:
    for key in create_locks:
        distlock.delete_lock(key)
