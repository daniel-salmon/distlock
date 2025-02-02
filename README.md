# distlock
Implements a distributed lock client and server.

This is particularly useful for situations where you need efficiency gains when
running tasks in a distributed environment, yet it is not catastrophic if
multiple workers attempt to run the same task at the same time. If you have a
workload that requires at most one worker to run a task at a time, you should
use a different distributed lock implementation. Unfortunately, this project
does not use replication / consensus on the backend, so if the server is
unavailable, there is no fallback mechanism since there is only one server. Put
differently, you should not use this for mission critical workloads.

# Table of Contents

- [Usage](#usage)
  - [Threaded Server](#threaded-server)
  - [Async Server](#async-server)
- [Client](#client)
- [Server](#server)

## Usage <a name="usage"></a>

You have two options for running the server: threaded or async. Both options use
gRPC for communication, the difference is only in how the server is implemented.

The complete usage is:
```sh
$ distlock --help

 Usage: distlock [OPTIONS]

╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --version               --no-version             Print the version number and exit [default: no-version]                             │
│ --address                               TEXT     Address on which to run the server [default: [::]]                                  │
│ --port                                  INTEGER  Port on which to run the server [default: 50051]                                    │
│ --max-workers                           INTEGER  Maximum number of workers for multithreaded server. Does not matter when running    │
│                                                  with --run-async.                                                                   │
│                                                  [default: 5]                                                                        │
│ --run-async                                      Should the server be run async?                                                     │
│ --install-completion                             Install completion for the current shell.                                           │
│ --show-completion                                Show completion for the current shell, to copy it or customize the installation.    │
│ --help                                           Show this message and exit.                                                         │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

### Threaded Server <a name="threaded-server"></a>

The threaded server is the default and can be run with the following command:

```bash
$ distlock
```

You can configure how many workers the server will use by passing the
`--max-workers` flag.

### Async Server <a name="async-server"></a>

The async server can be toggled on by passing the `--run-async` flag, e.g.:

```bash
$ distlock --run-async
```

The async server does not run multiple workers, it runs a single worker that
handles all requests concurrently. Therefore the `--max-workers` flag is not
used.


## Client <a name="client"></a>

The client is used to interact with the server. It can be used to create a new
lock, acquire it, or release it. The client has an async implementation in
situations where it needs to be used in an async context.

The main workflow is:

* Create a new lock: `distlock.create_lock(key="my_lock")`
* Acquire the lock: `distlock.acquire_lock(key="my_lock", expires_in_seconds=5)`
* Release the lock: `distlock.release_lock(Lock(key="my_lock"))`

When attempting to acquire the lock, you have the choice to block by specifying
`blocking=True`. By default blocking will happen indefinitely, however you can
configure the `timeout_seconds` so that after that amount of time a
`TimeoutError` will be raised. Specifying `heartbeat_seconds` will determine how
often the client will query the server to check if the lock is available and can
be acquired.

A full example:

```python
import sys

from distlock import Distlock

distlock = Distlock(address="localhost", port=50051)
distlock.create_lock(key="my_lock")

# This will block for at most 10 seconds
# If the lock is not available after 10 seconds, a TimeoutError will be raised
try:
    lock = distlock.acquire_lock(
        key="my_lock",
        expires_in_seconds=5,
        blocking=True,
        timeout_seconds=10,
        heartbeat_seconds=5,
    )
except TimeoutError:
    print("Could not acquire lock")
    sys.exit(1)

# Do some work
# You have 5 seconds to do your work before the server will be able to lease the
# lock to another worker

# Release the lock
distlock.release_lock(lock)
```

## Server <a name="server"></a>

The server maintains a collection of all locks that have been created and allows
workers to lease locks. Each lock maintains a logical, integer clock that gets
incremented with every lease. When a client attempts to release a lock it
presents the clock value it had when it leased the lock. The clock value is used
by the server to determine if the lock can be released by that client -- if the
lock was expired by the time the client requests to release the lock, it's
possible another client has leased the lock in the meantime.

To be more specific, maintaining a clock is useful because it is possible that
client A leased the lock and was unable to release the lock before the lock
expired. If client B leased the lock before client A could release it, client A
should not be able to release the lock (it's possible client B is still working
and also client A should know that it no longer has exclusive access to the lock
and may need to take cleanup actions). The server can determine this by
comparing the logical clock value whenever a client attempts to release a lock.
In this case, when client B leased the lock, the server incremented the clock
value to one more than the clock value client A had when it leased the lock.
Then when client A attempts to release the lock, the server will see that A's
clock is behind and will let client A know that it could not release the lock by
returning an `UnreleasableError` to client A. This allows client A to know it
did not have exclusive access to the lock since it did not release the lock
within the expiration time it requested when it leased the lock.

The clock value on the lock can also be used by clients when writing data. It
can provide a way to resolve write orders when two workers both acquired the
same lock after a slow client A did not release the lock before it expired, and
yet both clients attempt to write data to the same resource. Writes can be
resolved by using the write value that is associated with a higher lock value,
since the client with the higher lock value must be associated with the worker
that has the most recent lease on the lock.
