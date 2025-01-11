import grpc

from distlock.stubs.distlock_pb2 import EmptyRequest
from distlock.stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: int = 50051):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        list_locks = stub.ListLocks(EmptyRequest())
        locks = list_locks.locks
        print(f"Fetched {len(locks)} locks")
        for lock in locks:
            print(lock)


if __name__ == "__main__":
    run()
