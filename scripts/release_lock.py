import sys

import grpc

from distlock.stubs.distlock_pb2 import Lock
from distlock.stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: int = 50051, key: str = "a_lock", clock: int = 1):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        try:
            stub.ReleaseLock(Lock(key=key, clock=clock))
        except grpc.RpcError as e:
            if grpc.StatusCode.ABORTED == e.code():
                print(e.details())
                return
            if grpc.StatusCode.NOT_FOUND == e.code():
                print(f"Lock by the name {key} does not exist")
                return
            raise
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
