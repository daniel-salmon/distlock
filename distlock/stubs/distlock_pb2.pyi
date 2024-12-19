from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EmptyResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Lock(_message.Message):
    __slots__ = ("key", "clock")
    KEY_FIELD_NUMBER: _ClassVar[int]
    CLOCK_FIELD_NUMBER: _ClassVar[int]
    key: str
    clock: int
    def __init__(self, key: _Optional[str] = ..., clock: _Optional[int] = ...) -> None: ...

class AcquireLockRequest(_message.Message):
    __slots__ = ("key", "timeout_seconds")
    KEY_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_SECONDS_FIELD_NUMBER: _ClassVar[int]
    key: str
    timeout_seconds: int
    def __init__(self, key: _Optional[str] = ..., timeout_seconds: _Optional[int] = ...) -> None: ...
