import time

import grpc

from .exceptions import AlreadyExistsError, NotFoundError, UnreleasableError
from .models import Lock
from .stubs import distlock_pb2
from .stubs.distlock_pb2_grpc import DistlockStub


class Distlock:
    def __init__(self, address: str = "[::]", port: int = 50051):
        self._address = f"{address}:{port}"

    def acquire_lock(
        self,
        key: str,
        expires_in_seconds: int,
        blocking: bool = True,
        timeout_seconds: float = -1.0,
        heartbeat_seconds: float = 3.0,
    ) -> Lock:
        timeout = (
            time.time() + timeout_seconds if timeout_seconds >= 0 else float("inf")
        )
        with grpc.insecure_channel(self._address) as channel:
            stub = DistlockStub(channel)
            while True:
                try:
                    lock = Lock.from_pb(
                        stub.AcquireLock(
                            distlock_pb2.AcquireLockRequest(
                                key=key,
                                expires_in_seconds=expires_in_seconds,
                            ),
                        ),
                    )
                except grpc.RpcError as e:
                    if e.code() == grpc.StatusCode.NOT_FOUND:
                        raise NotFoundError(
                            f"Lock by the name {key} does not exist on the server"
                        )
                    raise
                if lock.acquired or not blocking:
                    break
                if time.time() > timeout:
                    raise TimeoutError(
                        f"Unable to acquire a lock on {key} within the timeout"
                    )
                time.sleep(heartbeat_seconds)
        return lock

    def create_lock(self, key: str) -> None:
        with grpc.insecure_channel(self._address) as channel:
            stub = DistlockStub(channel)
            try:
                _ = stub.CreateLock(distlock_pb2.Lock(key=key))
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                    raise AlreadyExistsError(
                        f"Lock by the name {key} already exists on the server"
                    )
                raise

    def delete_lock(self, key: str) -> None:
        with grpc.insecure_channel(self._address) as channel:
            stub = DistlockStub(channel)
            try:
                _ = stub.DeleteLock(distlock_pb2.Lock(key=key))
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    raise NotFoundError(
                        f"Lock by the name {key} does not exist on the server"
                    )
                raise

    def get_lock(self, key: str) -> Lock:
        with grpc.insecure_channel(self._address) as channel:
            stub = DistlockStub(channel)
            try:
                lock = Lock.from_pb(stub.GetLock(distlock_pb2.Lock(key=key)))
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.NOT_FOUND:
                    raise NotFoundError(
                        f"Lock by the name {key} does not exist on the server"
                    )
                raise
        return lock

    def list_locks(self) -> list[Lock]:
        with grpc.insecure_channel(self._address) as channel:
            stub = DistlockStub(channel)
            locks = [
                Lock.from_pb(lock)
                for lock in stub.ListLocks(distlock_pb2.EmptyRequest()).locks
            ]
        return locks

    def release_lock(self, lock: Lock) -> None:
        with grpc.insecure_channel(self._address) as channel:
            stub = DistlockStub(channel)
            try:
                _ = stub.ReleaseLock(lock.to_pb())
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.ABORTED:
                    raise UnreleasableError(e.details())
                elif e.code() == grpc.StatusCode.NOT_FOUND:
                    raise NotFoundError(f"Lock by the name {lock.key} does not exist")
                raise
        return
