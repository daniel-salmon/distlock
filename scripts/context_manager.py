from distlock import Distlock, NotFoundError


def run(
    address: str = "[::]",
    port: int = 50051,
    key: str = "a_lock",
    expires_in_seconds: int = 0,
    blocking: bool = True,
) -> None:
    distlock = Distlock(address, port)
    try:
        lock = distlock.get_lock(key)
    except NotFoundError:
        print(f"Lock by the name {key} does not exist")
        return
    with lock as my_lock:
        print(f"Lock {key} acquired:\n{my_lock}")
    print("Released lock")
