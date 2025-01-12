import shlex
import subprocess
import time
from typing import Generator

import pytest


# NOTE: It is possible that you will need to kill the process opened here manually.
# For example, if you happen to introduce a bug in this function, the process may never be terminated.
# In such cases you can terminate the process by finding all open socket files on port 50051:
# sudo lsof -ti :50051
# You can then kill that. It's possible you forgot to kill some other processes which
# may still be running and listening on that port, which may be causing you some errors in your tests.
# To do so you can kill all processes listening on that port with
# sudo lsof -ti :50051 | xargs kill -9
@pytest.fixture(scope="session")
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
