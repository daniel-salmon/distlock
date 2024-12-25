from datetime import datetime, timedelta, timezone

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel

from .stubs import distlock_pb2

EPOCH_START = datetime(
    year=1970,
    month=1,
    day=1,
    tzinfo=timezone.utc,
)


class Lock(BaseModel):
    key: str = ""
    acquired: bool = False
    clock: int = 0
    timeout: datetime = EPOCH_START

    def acquire(self, timeout_seconds: int) -> None:
        self.acquired = True
        self.clock += 1
        self.timeout = datetime.now(timezone.utc) + timedelta(seconds=timeout_seconds)

    def to_pb_Lock(self) -> distlock_pb2.Lock:
        timeout = Timestamp()
        timeout.FromDatetime(self.timeout)
        return distlock_pb2.Lock(
            key=self.key,
            acquired=self.acquired,
            clock=self.clock,
            timeout=timeout,
        )
