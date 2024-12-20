import sys

import grpc

from distlock.stubs.distlock_pb2 import AcquireLockRequest
from distlock.stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: int = 50051, key: str = "a_lock"):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        try:
            lock = stub.AcquireLock(AcquireLockRequest(key=key))
        except grpc.RpcError as e:
            if grpc.StatusCode.NOT_FOUND == e.code():
                print(f"Lock by the name {key} does not exist")
                return
            raise
        if lock.acquired:
            print(f"Lock {key} acquired:\n{lock}")
        else:
            print(
                f"Lock by the name {key} is acquired by someone else. Will be available at {lock.timeout.ToDatetime()}"
            )


if __name__ == "__main__":
    if len(sys.argv) == 1:
        key = "a_lock"
    else:
        key = sys.argv[1]
    run(key=key)
