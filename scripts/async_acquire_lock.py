import asyncio
import sys

from distlock import DistlockAsync, NotFoundError


async def run(
    address: str = "[::]",
    port: int = 50051,
    key: str = "a_lock",
    expires_in_seconds: int = 0,
    blocking: bool = True,
):
    distlock = DistlockAsync(address, port)
    try:
        lock = await distlock.acquire_lock(
            key=key,
            expires_in_seconds=expires_in_seconds,
            blocking=blocking,
        )
    except NotFoundError:
        print(f"Lock by the name {key} does not exist")
        return
    print(f"Lock {key} acquired:\n{lock}")


if __name__ == "__main__":
    key = "a_lock"
    expires_in_seconds = 0
    blocking = True
    if len(sys.argv) == 2:
        key = sys.argv[1]
    elif len(sys.argv) == 3:
        key = sys.argv[1]
        expires_in_seconds = int(sys.argv[2])
    elif len(sys.argv) == 4:
        key = sys.argv[1]
        expires_in_seconds = int(sys.argv[2])
        blocking = bool(sys.argv[3])
    asyncio.run(run(key=key, expires_in_seconds=expires_in_seconds, blocking=blocking))
