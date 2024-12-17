import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import grpc

from .lock_store import LockStore
from .stubs.distlock_pb2 import CreateLockRequest, EmptyResponse
from .stubs.distlock_pb2_grpc import DistlockServicer, add_DistlockServicer_to_server

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s.%(msecs)03d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


lock_store = LockStore()


class Servicer(DistlockServicer):
    def CreateLock(
        self, request: CreateLockRequest, context: grpc.ServicerContext
    ) -> EmptyResponse:
        if request.key in lock_store:
            context.set_details(f"A lock with the key {request.key} already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return EmptyResponse()
        lock_store[request.key] = Lock()
        logger.info(f"Created lock named {request.key}")
        return EmptyResponse()


def serve(address: str = "[::]", port: str = "50051", max_workers: int = 5):
    server = grpc.server(ThreadPoolExecutor(max_workers=max_workers))
    add_DistlockServicer_to_server(Servicer(), server)
    server.add_insecure_port(f"{address}:{port}")
    server.start()
    logger.info(f"Server started on {address}:{port}")
    server.wait_for_termination()
