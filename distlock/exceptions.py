class AlreadyAcquiredError(Exception):
    pass


class AlreadyExistsError(KeyError):
    pass


class NotFoundError(Exception):
    pass


class UnreleasableError(Exception):
    pass
