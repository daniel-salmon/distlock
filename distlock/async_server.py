import logging

import grpc

from .lock_store import LockStore
from .stubs import distlock_pb2, distlock_pb2_grpc

ONE_MINUTE_IN_SECONDS = 1 * 60

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s.%(msecs)03d %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


class AsyncServicer(distlock_pb2_grpc.DistlockServicer):
    def __init__(self):
        self.lock_store = LockStore()

    async def CreateLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        return distlock_pb2.EmptyResponse()

    async def AcquireLock(
        self,
        request: distlock_pb2.AcquireLockRequest,
        context: grpc.aio.ServicerContext,
    ) -> distlock_pb2.Lock:
        return distlock_pb2.Lock()

    async def ReleaseLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        return distlock_pb2.EmptyResponse()

    async def GetLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.Lock:
        return distlock_pb2.Lock()

    async def ListLocks(
        self, request: distlock_pb2.EmptyRequest, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.Locks:
        return distlock_pb2.Locks()

    async def DeleteLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        return distlock_pb2.EmptyResponse()


async def serve(*, address: str, port: int):
    server = grpc.aio.server()
    distlock_pb2_grpc.add_DistlockServicer_to_server(AsyncServicer(), server)
    server.add_insecure_port(f"{address}:{port}")
    logger.info(f"Starting server on {address}:{port}")
    await server.start()
    await server.wait_for_termination()
