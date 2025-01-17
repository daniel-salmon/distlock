import asyncio
import sys

from distlock import AlreadyExistsError, DistlockAsync


async def run(address: str = "[::]", port: int = 50051, key: str = "a_lock"):
    distlock = DistlockAsync(address, port)
    try:
        await distlock.create_lock(key)
    except AlreadyExistsError:
        print(f"Lock by the name {key} already exists on the server")
        return
    print(f"Lock {key} created")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        key = "a_lock"
    else:
        key = sys.argv[1]
    asyncio.run(run(key=key))
