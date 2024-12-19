from datetime import datetime


class AlreadyAcquiredError(Exception):
    def __init__(self, timeout: datetime | None):
        super().__init__()
        self.timeout = timeout


class AlreadyExistsError(KeyError):
    pass
