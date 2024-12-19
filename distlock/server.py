import logging
from concurrent.futures import ThreadPoolExecutor

import grpc

from .exceptions import AlreadyExistsError
from .lock_store import LockStore
from .models import Lock
from .stubs import distlock_pb2, distlock_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s.%(msecs)03d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Servicer(distlock_pb2_grpc.DistlockServicer):
    def __init__(self):
        self.lock_store = LockStore()

    def CreateLock(
        self, request: distlock_pb2.Lock, context: grpc.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        try:
            self.lock_store.set_not_exists(
                request.key, Lock(acquired=False, clock=0, timeout=None)
            )
        except AlreadyExistsError:
            context.set_details(f"A lock with the key {request.key} already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return distlock_pb2.EmptyResponse()
        logger.info(f"Created lock named {request.key}")
        return distlock_pb2.EmptyResponse()

    def AcquireLock(
        self, request: distlock_pb2.AcquireLockRequest, context: grpc.ServicerContext
    ) -> distlock_pb2.Lock:
        return distlock_pb2.Lock()

    def ReleaseLock(
        self, request: distlock_pb2.Lock, context: grpc.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        return distlock_pb2.EmptyResponse()


def serve(address: str = "[::]", port: int = 50051, max_workers: int = 5):
    server = grpc.server(ThreadPoolExecutor(max_workers=max_workers))
    distlock_pb2_grpc.add_DistlockServicer_to_server(Servicer(), server)
    server.add_insecure_port(f"{address}:{port}")
    server.start()
    logger.info(f"Server started on {address}:{port}")
    server.wait_for_termination()
