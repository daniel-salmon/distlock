from __future__ import annotations

from datetime import datetime, timedelta, timezone
from types import TracebackType
from typing import Self

from google.protobuf.timestamp_pb2 import Timestamp
from pydantic import BaseModel

from .client import Distlock
from .exceptions import UnreleasableError
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
    distlock: Distlock | None = None
    acquired_lock: Lock | None = None

    def __enter__(self) -> None:
        assert self.distlock is not None
        self.acquired_lock = self.distlock.acquire_lock(
            key=self.key,
            expires_in_seconds=3,
            blocking=True,
        )

    def __exit__(
        self,
        exc_type: BaseException | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        assert self.acquired_lock is not None
        assert self.distlock is not None
        self.distlock.release_lock(self.acquired_lock)
        self.distlock = None
        self.acquired_lock = None

    def acquire(self, expires_in_seconds: int) -> None:
        self.acquired = True
        self.clock += 1
        self.expires_at = datetime.now(timezone.utc) + timedelta(
            seconds=expires_in_seconds
        )

    @property
    def expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

    def release(self, clock: int) -> None:
        if clock != self.clock:
            raise UnreleasableError(
                f"Tried to release lock at clock {self.clock}, but given clock {clock}. Perhaps client is out of sync?"
            )
        self.acquired = False

    @classmethod
    def from_pb(cls, lock: distlock_pb2.Lock) -> Self:
        new_lock = cls(
            key=lock.key,
            acquired=lock.acquired,
            clock=lock.clock,
            expires_at=lock.expires_at.ToDatetime(),
        )
        return new_lock

    def to_pb(self) -> distlock_pb2.Lock:
        expires_at = Timestamp()
        expires_at.FromDatetime(self.expires_at)
        return distlock_pb2.Lock(
            key=self.key,
            acquired=self.acquired,
            clock=self.clock,
            expires_at=expires_at,
        )
