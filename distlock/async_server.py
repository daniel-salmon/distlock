import logging

import grpc

from .exceptions import AlreadyExistsError, UnreleasableError
from .lock_store import ThreadSafeLockStore
from .models import Lock
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
        self.lock_store = ThreadSafeLockStore()

    async def CreateLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        logger.info(f"Received request to create lock named {request.key}")
        try:
            self.lock_store.set_not_exists(
                request.key,
                Lock(key=request.key),
            )
        except AlreadyExistsError:
            msg = f"A lock with key {request.key} already exists"
            logger.error(msg)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            return distlock_pb2.EmptyResponse()
        logger.info(f"Created lock named {request.key}")
        return distlock_pb2.EmptyResponse()

    async def AcquireLock(
        self,
        request: distlock_pb2.AcquireLockRequest,
        context: grpc.aio.ServicerContext,
    ) -> distlock_pb2.Lock:
        logger.info(
            f"Received request to acquire lock named {request.key} with an expires in of {request.expires_in_seconds} seconds"
        )
        if request.expires_in_seconds != 0:
            expires_in_seconds = request.expires_in_seconds
        else:
            expires_in_seconds = ONE_MINUTE_IN_SECONDS
        try:
            lock = self.lock_store.acquire(
                key=request.key,
                expires_in_seconds=expires_in_seconds,
            )
        except KeyError:
            msg = f"A lock with key {request.key} does not exist"
            logger.error(msg)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return distlock_pb2.Lock()
        logger.info(
            f"Lock with key {request.key} has {'' if lock.acquired else 'not'} been acquired"
        )
        return lock.to_pb()

    async def ReleaseLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        logger.info(f"Received request to release lock named {request.key}")
        try:
            self.lock_store.release(
                key=request.key,
                clock=request.clock,
            )
            logger.info(f"Lock with key {request.key} has been released")
        except UnreleasableError as e:
            msg = f"Could not release lock: {e}"
            logger.error(msg)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.ABORTED)
            return distlock_pb2.EmptyResponse()
        except KeyError:
            msg = f"A lock with key {request.key} does not exist"
            logger.error(msg)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return distlock_pb2.EmptyResponse()
        return distlock_pb2.EmptyResponse()

    async def GetLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.Lock:
        logger.info(f"Received request to fetch lock named {request.key}")
        try:
            lock = self.lock_store[request.key]
            logger.info(f"Lock with key {lock.key} has been fetched")
        except KeyError:
            msg = f"A lock with key {request.key} does not exist"
            logger.error(msg)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return request
        return lock.to_pb()

    async def ListLocks(
        self, request: distlock_pb2.EmptyRequest, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.Locks:
        logger.info("Received request to list locks")
        locks = [lock.to_pb() for lock in self.lock_store.to_list()]
        return distlock_pb2.Locks(locks=locks)

    async def DeleteLock(
        self, request: distlock_pb2.Lock, context: grpc.aio.ServicerContext
    ) -> distlock_pb2.EmptyResponse:
        logger.info(f"Received request to delete lock with key {request.key}")
        try:
            del self.lock_store[request.key]
            logger.info(f"Lock with key {request.key} has been deleted")
        except KeyError:
            msg = f"A lock with key {request.key} does not exist"
            logger.error(msg)
            context.set_details(msg)
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return distlock_pb2.EmptyResponse()
        return distlock_pb2.EmptyResponse()


async def serve(
    *,
    address: str,
    port: int,
    cleanup_coroutines: list,
    graceful_shutdown_period_seconds: float = 1,
):
    server = grpc.aio.server()
    distlock_pb2_grpc.add_DistlockServicer_to_server(AsyncServicer(), server)
    server.add_insecure_port(f"{address}:{port}")
    logger.info(f"Starting server on {address}:{port}")
    await server.start()

    async def server_graceful_shutdown():
        logger.info("Starting graceful shutdown")
        await server.stop(graceful_shutdown_period_seconds)

    cleanup_coroutines.append(server_graceful_shutdown())

    await server.wait_for_termination()
