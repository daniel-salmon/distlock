import asyncio
import sys

from distlock import DistlockAsync, NotFoundError


async def run(address: str = "[::]", port: int = 50051, key: str = "a_lock"):
    distlock = DistlockAsync(address, port)
    try:
        lock = await distlock.get_lock(key)
    except NotFoundError:
        print(f"Lock by the name {key} does not exist")
        return
    print(f"Lock fetched:\n{lock}")


if __name__ == "__main__":
    key = "a_lock"
    if len(sys.argv) > 1:
        key = sys.argv[1]
    asyncio.run(run(key=key))
