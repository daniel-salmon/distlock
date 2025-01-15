import subprocess
from typing import Generator

import pytest

from distlock import Distlock, NotFoundError


@pytest.fixture(scope="function")
def distlock(distlock_server: subprocess.Popen) -> Distlock:
    return Distlock()


@pytest.fixture(scope="function")
def create_locks(distlock: Distlock) -> Generator[list[str], None, None]:
    keys = ["key1", "key2", "key3"]
    for key in keys:
        distlock.create_lock(key)
    yield keys
    cleanup(distlock, keys)


def cleanup(distlock: Distlock, keys: list[str]) -> None:
    for key in keys:
        try:
            distlock.delete_lock(key)
        except NotFoundError:
            # The key may have already been deleted, which is fine
            pass
    lock_names = {lock.key for lock in distlock.list_locks()}
    assert len(lock_names) == len(lock_names - set(keys))
