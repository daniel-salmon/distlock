import sys

from distlock import Distlock, Lock, NotFoundError, UnreleasableError


def run(address: str = "[::]", port: int = 50051, key: str = "a_lock", clock: int = 1):
    distlock = Distlock(address, port)
    try:
        distlock.release_lock(Lock(key=key, clock=clock))
    except NotFoundError:
        print(f"Lock by the name {key} does not exist")
        return
    except UnreleasableError as e:
        print(e)
        return
    print(f"Lock by the name {key} has been released")


if __name__ == "__main__":
    key = "a_lock"
    clock = 1
    if len(sys.argv) == 2:
        key = sys.argv[1]
    elif len(sys.argv) > 2:
        key = sys.argv[1]
        clock = int(sys.argv[2])
    run(key=key, clock=clock)
