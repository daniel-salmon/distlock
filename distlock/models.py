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
    expires_at: datetime = EPOCH_START

    def acquire(self, expires_in_seconds: int) -> None:
        self.acquired = True
        self.clock += 1
        self.expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=expires_in_seconds
        )

    @property
    def expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

    def to_pb_Lock(self) -> distlock_pb2.Lock:
        expires_at = Timestamp()
        expires_at.FromDatetime(self.expires_at)
        return distlock_pb2.Lock(
            key=self.key,
            acquired=self.acquired,
            clock=self.clock,
            expires_at=expires_at,
        )
