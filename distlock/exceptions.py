class AlreadyAcquiredError(Exception):
    pass


class AlreadyExistsError(KeyError):
    pass


class UnreleasableError(Exception):
    pass
