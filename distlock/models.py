from datetime import datetime

from pydantic import BaseModel


class Mutex(BaseModel):
    acquired: bool = False
    clock: int = 0
    timeout: datetime | None = None
