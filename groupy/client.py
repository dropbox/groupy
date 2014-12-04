from clowncar.backends import Backends
import json
from threading import Lock
import time
from tornado.httpclient import HTTPClient, HTTPError

from . import exc
from .collations import Users, Groups, Permissions


class Groupy(object):
    def __init__(self, servers, partition_key=None, timeout=3,
                 allow_time_travel=False, checkpoint=0, checkpoint_time=0,
                 max_drift=600, mark_bad_timeout=60, max_backend_tries=5):

        self._lock = Lock()
        self.timeout = timeout
        self.backends = Backends(servers, partition_key)

        self.checkpoint = checkpoint
        self.checkpoint = checkpoint_time

        self.allow_time_travel = allow_time_travel
        self.max_drift = max_drift
        self.mark_bad_timeout = mark_bad_timeout
        self.max_backend_tries = max_backend_tries

        self.users = Users(self, "users")
        self.groups = Groups(self, "groups")
        self.permissions = Permissions(self, "permissions")

    def _try_get(self, path):
        for idx in range(self.max_backend_tries):
            try:
                return self._get(path)
            except exc.BackendConnectionError as err:
                self.backends.mark_dead(err.server, self.mark_bad_timeout)
        raise exc.BackendConnectionError(
            "Tried {} servers, all failed.".format(self.max_backend_tries),
            err.server
        )

    def _get(self, path):
        http_client = HTTPClient()
        server = self.backends.server
        url = "http://{}:{}{}".format(server.hostname, server.port, path)
        try:
            out = json.loads(http_client.fetch(url, **{
                "connect_timeout": self.timeout,
                "request_timeout": self.timeout,
            }).body)
        except HTTPError as err:
            if err.code == 599:
                raise exc.BackendConnectionError(err.message, server)
            try:
                out = json.loads(err.response.body)
                if "status" not in out:
                    raise exc.BackendIntegrityError(err.message, server)
            except (ValueError, TypeError):
                raise exc.BackendIntegrityError(err.message, server)

        now = time.time()
        drift = now - out["checkpoint_time"]
        if self.max_drift is not None and self.max_drift > abs(drift):
            raise exc.BackendMaxDriftError(
                "Backend last checkpoint stale by {} seconds.".format(drift),
                server
            )

        with self._lock:
            new_checkpoint = out["checkpoint"]
            old_checkpoint = self.checkpoint
            if new_checkpoint < old_checkpoint and not self.allow_time_travel:
                raise exc.TimeTravelNotAllowed(
                    "Received checkpoint of {} when previously {}".format(
                        new_checkpoint, old_checkpoint
                    ), server
                )
            self.checkpoint = new_checkpoint

        return out
