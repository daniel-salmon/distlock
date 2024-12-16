import grpc

from .stubs.distlock_pb2 import CreateLockRequest
from .stubs.distlock_pb2_grpc import DistlockStub


def run(address: str = "[::]", port: str = "50051", name: str = "a_lock"):
    with grpc.insecure_channel(f"{address}:{port}") as channel:
        stub = DistlockStub(channel)
        _ = stub.CreateLock(CreateLockRequest(name=name))
        print("Lock created")


if __name__ == "__main__":
    run()
