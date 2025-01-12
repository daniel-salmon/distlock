import subprocess

import pytest

from distlock import Distlock


def cleanup(distlock: Distlock, keys: list[str]) -> None:
    for key in keys:
        distlock.delete_lock(key)
    lock_names = {lock.key for lock in distlock.list_locks()}
    assert len(lock_names) == len(lock_names - set(keys))


@pytest.mark.parametrize("key", ["key", "different key", "one more key"])
def test_create_lock(key: str, distlock_server: subprocess.Popen) -> None:
    distlock = Distlock()
    distlock.create_lock(key)
    cleanup(distlock, keys=[key])


@pytest.mark.parametrize(
    "keys",
    [
        ["key1", "key2", "key3"],
        ["value1", "value2", "value3"],
    ],
)
def test_create_locks(keys: list[str], distlock_server: subprocess.Popen) -> None:
    distlock = Distlock()
    for key in keys:
        distlock.create_lock(key)
    cleanup(distlock, keys=keys)
