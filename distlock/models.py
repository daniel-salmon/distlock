from datetime import datetime, timedelta, timezone

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel

from .stubs import distlock_pb2

ONE_MINUTE_IN_SECONDS = 1 * 60


class Lock(BaseModel):
    key: str = ""
    acquired: bool = False
    clock: int = 0
    # NOTE: May later decide to default this to start of Unix epoch
    timeout: datetime | None = None

    def acquire(self, timeout_seconds: int | None) -> None:
        if timeout_seconds is None:
            timeout_seconds = ONE_MINUTE_IN_SECONDS
        self.acquired = True
        self.clock += 1
        self.timeout = datetime.now(timezone.utc) + timedelta(seconds=timeout_seconds)

    def to_pb_Lock(self) -> distlock_pb2.Lock:
        timeout = Timestamp()
        if self.timeout is not None:
            timeout.FromDatetime(self.timeout)
        return distlock_pb2.Lock(
            key=self.key,
            acquired=self.acquired,
            clock=self.clock,
            timeout=timeout,
        )
