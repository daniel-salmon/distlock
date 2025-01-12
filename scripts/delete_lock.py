import sys

from distlock import Distlock, NotFoundError


def run(address: str = "[::]", port: int = 50051, key: str = "a_lock"):
    distlock = Distlock(address, port)
    try:
        distlock.delete_lock(key)
    except NotFoundError:
        print(f"Lock by the name {key} does not exist")
        return
    print("Lock deleted")


if __name__ == "__main__":
    key = "a_lock"
    if len(sys.argv) > 1:
        key = sys.argv[1]
    run(key=key)
