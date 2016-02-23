class Error(Exception):
    pass


class BackendError(Error):
    def __init__(self, message, server):
        self.message = message
        self.server = server

    def __str__(self):
        return "({}:{}) - {}".format(
            self.server.hostname, self.server.port, self.message
        )


class BackendConnectionError(BackendError):
    pass


class BackendIntegrityError(BackendError):
    pass


class TimeTravelNotAllowed(BackendError):
    pass


class BackendMaxDriftError(BackendError):
    pass


class ResourceError(Error):
    pass


class ResourceNotFound(ResourceError):
    pass
