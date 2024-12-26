from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmptyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Lock(_message.Message):
    __slots__ = ("key", "acquired", "clock", "expires_at")
    KEY_FIELD_NUMBER: _ClassVar[int]
    ACQUIRED_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    key: str
    acquired: bool
    clock: int
    expires_at: _timestamp_pb2.Timestamp
    def __init__(self, key: _Optional[str] = ..., acquired: bool = ..., clock: _Optional[int] = ..., expires_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class AcquireLockRequest(_message.Message):
    __slots__ = ("key", "expires_in_seconds")
    KEY_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_SECONDS_FIELD_NUMBER: _ClassVar[int]
    key: str
    expires_in_seconds: int
    def __init__(self, key: _Optional[str] = ..., expires_in_seconds: _Optional[int] = ...) -> None: ...
