import asyncio

from distlock import DistlockAsync


async def run(address: str = "[::]", port: int = 50051):
    distlock = DistlockAsync(address, port)
    locks = await distlock.list_locks()
    print(f"Fetched {len(locks)} locks")
    for lock in locks:
        print(lock)


if __name__ == "__main__":
    asyncio.run(run())
