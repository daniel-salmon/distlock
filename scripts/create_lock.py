import sys

import grpc

from distlock.stubs.distlock_pb2 import Lock
from distlock.stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: int = 50051, key: str = "a_lock"):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        try:
            _ = stub.CreateLock(Lock(key=key))
        except grpc.RpcError as e:
            if grpc.StatusCode.ALREADY_EXISTS == e.code():
                print(f"Lock by the name {key} already exists")
                return
            raise
        print(f"Lock {key} created")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        key = "a_lock"
    else:
        key = sys.argv[1]
    run(key=key)
