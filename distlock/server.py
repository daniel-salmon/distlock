import logging
from concurrent.futures import ThreadPoolExecutor

import grpc

from .exceptions import AlreadyExistsError
from .lock_store import LockStore
from .models import Mutex
from .stubs.distlock_pb2 import EmptyResponse, Lock
from .stubs.distlock_pb2_grpc import DistlockServicer, add_DistlockServicer_to_server

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s.%(msecs)03d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class Servicer(DistlockServicer):
    def __init__(self):
        self.lock_store = LockStore()

    def CreateLock(self, request: Lock, context: grpc.ServicerContext) -> EmptyResponse:
        try:
            self.lock_store.set_not_exists(
                request.key, Mutex(acquired=False, clock=0, timeout=None)
            )
        except AlreadyExistsError:
            context.set_details(f"A lock with the key {request.key} already exists")
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return EmptyResponse()
        logger.info(f"Created lock named {request.key}")
        return EmptyResponse()


def serve(address: str = "[::]", port: int = 50051, max_workers: int = 5):
    server = grpc.server(ThreadPoolExecutor(max_workers=max_workers))
    add_DistlockServicer_to_server(Servicer(), server)
    server.add_insecure_port(f"{address}:{port}")
    server.start()
    logger.info(f"Server started on {address}:{port}")
    server.wait_for_termination()
