from datetime import datetime


class AlreadyAcquiredError(Exception):
    def __init__(self, message: str, timeout: datetime | None):
        super().__init__(message)
        self.timeout = timeout


class AlreadyExistsError(KeyError):
    pass
