import shlex
import subprocess
import time
from typing import Generator

import pytest

from distlock import Distlock, DistlockAsync, NotFoundError


# NOTE: It is possible that you will need to kill the process opened here manually.
# For example, if you happen to introduce a bug in this function, the process may never be terminated.
# In such cases you can terminate the process by finding all open socket files on port 50051:
# sudo lsof -ti :50051
# You can then kill that. It's possible you forgot to kill some other processes which
# may still be running and listening on that port, which may be causing you some errors in your tests.
# To do so you can kill all processes listening on that port with
# sudo lsof -ti :50051 | xargs kill -9
@pytest.fixture(scope="module")
def distlock_server() -> Generator[subprocess.Popen, None, None]:
    command = shlex.split("python -m distlock")
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # Wait for server to start up
    time.sleep(1)

    yield process

    process.terminate()
    process.wait()
    assert process.stdout is not None
    print(process.stdout.read())


@pytest.fixture(scope="function")
def distlock(distlock_server: subprocess.Popen) -> Distlock:
    return Distlock()


@pytest.fixture(scope="function")
def distlock_async(distlock_server: subprocess.Popen) -> DistlockAsync:
    return DistlockAsync()


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


async def cleanup_async(distlock_async: DistlockAsync, keys: list[str]) -> None:
    for key in keys:
        try:
            await distlock_async.delete_lock(key)
        except NotFoundError:
            # The key may have already been deleted which is fine
            pass
    locks = await distlock_async.list_locks()
    lock_names = {lock.key for lock in locks}
    assert len(lock_names) == len(lock_names - set(keys))
