from distlock import Distlock


def run(address: str = "[::]", port: int = 50051):
    distlock = Distlock(address, port)
    locks = distlock.list_locks()
    print(f"Fetched {len(locks)} locks")
    for lock in locks:
        print(lock)


if __name__ == "__main__":
    run()
