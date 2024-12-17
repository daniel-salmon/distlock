import grpc

from distlock.stubs.distlock_pb2 import CreateLockRequest
from distlock.stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: str = "50051", key: str = "a_lock"):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        try:
            _ = stub.CreateLock(CreateLockRequest(key=key))
        except grpc.RpcError as e:
            if grpc.StatusCode.ALREADY_EXISTS == e.code():
                print(f"Lock by the name {key} already exists")
                return
            raise
        print("Lock created")


if __name__ == "__main__":
    run()
