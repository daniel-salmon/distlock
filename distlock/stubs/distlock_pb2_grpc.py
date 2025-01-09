# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from . import distlock_pb2 as distlock__pb2

GRPC_GENERATED_VERSION = '1.68.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in distlock_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class DistlockStub(object):
    """A distributed lock service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateLock = channel.unary_unary(
                '/distlock.Distlock/CreateLock',
                request_serializer=distlock__pb2.Lock.SerializeToString,
                response_deserializer=distlock__pb2.EmptyResponse.FromString,
                _registered_method=True)
        self.AcquireLock = channel.unary_unary(
                '/distlock.Distlock/AcquireLock',
                request_serializer=distlock__pb2.AcquireLockRequest.SerializeToString,
                response_deserializer=distlock__pb2.Lock.FromString,
                _registered_method=True)
        self.ReleaseLock = channel.unary_unary(
                '/distlock.Distlock/ReleaseLock',
                request_serializer=distlock__pb2.Lock.SerializeToString,
                response_deserializer=distlock__pb2.EmptyResponse.FromString,
                _registered_method=True)
        self.GetLock = channel.unary_unary(
                '/distlock.Distlock/GetLock',
                request_serializer=distlock__pb2.Lock.SerializeToString,
                response_deserializer=distlock__pb2.Lock.FromString,
                _registered_method=True)
        self.ListLocks = channel.unary_unary(
                '/distlock.Distlock/ListLocks',
                request_serializer=distlock__pb2.EmptyRequest.SerializeToString,
                response_deserializer=distlock__pb2.Locks.FromString,
                _registered_method=True)
        self.DeleteLock = channel.unary_unary(
                '/distlock.Distlock/DeleteLock',
                request_serializer=distlock__pb2.Lock.SerializeToString,
                response_deserializer=distlock__pb2.EmptyResponse.FromString,
                _registered_method=True)


class DistlockServicer(object):
    """A distributed lock service
    """

    def CreateLock(self, request, context):
        """Creates a new lock with the given key on the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AcquireLock(self, request, context):
        """Acquires the lock with the given key from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReleaseLock(self, request, context):
        """Releases the lock with the given key from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetLock(self, request, context):
        """Fetches the lock with the given key from the server, without acquiring it.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListLocks(self, request, context):
        """Fetches all locks from the server, without acquiring any of them.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteLock(self, request, context):
        """Deletes the lock with the given key from the server.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DistlockServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateLock': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateLock,
                    request_deserializer=distlock__pb2.Lock.FromString,
                    response_serializer=distlock__pb2.EmptyResponse.SerializeToString,
            ),
            'AcquireLock': grpc.unary_unary_rpc_method_handler(
                    servicer.AcquireLock,
                    request_deserializer=distlock__pb2.AcquireLockRequest.FromString,
                    response_serializer=distlock__pb2.Lock.SerializeToString,
            ),
            'ReleaseLock': grpc.unary_unary_rpc_method_handler(
                    servicer.ReleaseLock,
                    request_deserializer=distlock__pb2.Lock.FromString,
                    response_serializer=distlock__pb2.EmptyResponse.SerializeToString,
            ),
            'GetLock': grpc.unary_unary_rpc_method_handler(
                    servicer.GetLock,
                    request_deserializer=distlock__pb2.Lock.FromString,
                    response_serializer=distlock__pb2.Lock.SerializeToString,
            ),
            'ListLocks': grpc.unary_unary_rpc_method_handler(
                    servicer.ListLocks,
                    request_deserializer=distlock__pb2.EmptyRequest.FromString,
                    response_serializer=distlock__pb2.Locks.SerializeToString,
            ),
            'DeleteLock': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteLock,
                    request_deserializer=distlock__pb2.Lock.FromString,
                    response_serializer=distlock__pb2.EmptyResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'distlock.Distlock', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('distlock.Distlock', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Distlock(object):
    """A distributed lock service
    """

    @staticmethod
    def CreateLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distlock.Distlock/CreateLock',
            distlock__pb2.Lock.SerializeToString,
            distlock__pb2.EmptyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AcquireLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distlock.Distlock/AcquireLock',
            distlock__pb2.AcquireLockRequest.SerializeToString,
            distlock__pb2.Lock.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReleaseLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distlock.Distlock/ReleaseLock',
            distlock__pb2.Lock.SerializeToString,
            distlock__pb2.EmptyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distlock.Distlock/GetLock',
            distlock__pb2.Lock.SerializeToString,
            distlock__pb2.Lock.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListLocks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distlock.Distlock/ListLocks',
            distlock__pb2.EmptyRequest.SerializeToString,
            distlock__pb2.Locks.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteLock(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/distlock.Distlock/DeleteLock',
            distlock__pb2.Lock.SerializeToString,
            distlock__pb2.EmptyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
