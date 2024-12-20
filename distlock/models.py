from datetime import datetime, timedelta, timezone

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel

from .exceptions import AlreadyAcquiredError
from .stubs import distlock_pb2

TEN_MINUTES_IN_SECONDS = 10 * 60


class Lock(BaseModel):
    key: str = ""
    acquired: bool = False
    clock: int = 0
    # NOTE: May default this to start of Unix epoch
    timeout: datetime | None = None

    def acquire(self, timeout_seconds: int = TEN_MINUTES_IN_SECONDS) -> None:
        if self.acquired:
            raise AlreadyAcquiredError
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
