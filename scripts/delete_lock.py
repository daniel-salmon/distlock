import sys

import grpc

from distlock.stubs.distlock_pb2 import Lock
from distlock.stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: int = 50051, key: str = "a_lock"):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        try:
            _ = stub.DeleteLock(Lock(key=key))
        except grpc.RpcError as e:
            if grpc.StatusCode.NOT_FOUND == e.code():
                print(f"Lock by the name {key} does not exist")
                return
            raise
        print("Lock deleted")


if __name__ == "__main__":
    key = "a_lock"
    if len(sys.argv) > 1:
        key = sys.argv[1]
    run(key=key)
