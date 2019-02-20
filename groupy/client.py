import errno
import json
import logging
import socket
import urllib
from collections import namedtuple
from threading import Lock

from clowncar.backends import Backends
from tornado.httpclient import HTTPClient, HTTPError, HTTPRequest

from . import exc
from .collations import Groups, Permissions, ServiceAccounts, Users


Checkpoint = namedtuple('Checkpoint', ['checkpoint', 'checkpoint_time'])


def _checkpoint_is_greater(a, b):
    """Ensure elements of checkpoint 'a' are all greater than or equal to those in
    checkpoint 'b'."""
    return all((x >= y) for x, y in zip(a, b))


class Groupy(object):
    def __init__(self, servers, partition_key=None, timeout=3,
                 allow_time_travel=False, checkpoint=0, checkpoint_time=0,
                 mark_bad_timeout=60, max_backend_tries=5):
        """
        The grouper client.

        Args:
            servers (list of clowncar.server.Server): available API servers
            partition_key (str): key to use for picking a server, None defaults
                to hostname
            timeout (int): connection and request sent to tornado's HTTPClient
            allow_time_travel (bool): allow checkpoint[_time] to go backwards
                in subsequent queries
            checkpoint (int): starting checkpoint
            checkpoint_time (float): starting checkpoint unix epoch time
            mark_bad_timeout (int): time in seconds to not use servers that
                have been marked as dead
            max_backend_tries (int): number of backend servers to try before
                giving up and raising a BackendConnectionError
        """

        self._lock = Lock()
        self.timeout = timeout
        self.backends = Backends(servers, partition_key)

        self.checkpoint = Checkpoint(checkpoint, checkpoint_time)

        self.allow_time_travel = allow_time_travel
        self.mark_bad_timeout = mark_bad_timeout
        self.max_backend_tries = max_backend_tries

        self.users = Users(self, "users")
        self.groups = Groups(self, "groups")
        self.permissions = Permissions(self, "permissions")
        self.service_accounts = ServiceAccounts(self, "service_accounts")

    def _try_fetch(self, path, **kwargs):
        for idx in range(self.max_backend_tries):
            try:
                return self._fetch(path, **kwargs)
            except exc.BackendConnectionError as err:
                logging.warning("Marking server {} as dead.".format(err.server.hostname))
                self.backends.mark_dead(err.server, self.mark_bad_timeout)
        raise exc.BackendConnectionError(
            "Tried {} servers, all failed.".format(self.max_backend_tries),
            err.server
        )

    def _fetch(self, path, **kwargs):
        http_client = HTTPClient()
        server = self.backends.server
        url = HTTPRequest(
            "http://{}:{}{}".format(server.hostname, server.port, path),
            connect_timeout=self.timeout,
            request_timeout=self.timeout,
            **kwargs
        )
        try:
            out = json.loads(http_client.fetch(url).body)
        except HTTPError as err:
            if err.code == 599:
                raise exc.BackendConnectionError(err.message, server)
            try:
                out = json.loads(err.response.body)
                if "status" not in out:
                    raise exc.BackendIntegrityError(err.message, server)
            except (ValueError, TypeError):
                raise exc.BackendIntegrityError(err.message, server)
        except socket.error as err:
            if err.errno == errno.ECONNREFUSED:
                raise exc.BackendConnectionError("socket error (Connection Refused)", server)
            raise

        with self._lock:
            new_checkpoint = Checkpoint(
                out["checkpoint"],
                out["checkpoint_time"]
            )
            old_checkpoint = self.checkpoint
            if not _checkpoint_is_greater(new_checkpoint, old_checkpoint) and \
                    not self.allow_time_travel:
                raise exc.TimeTravelNotAllowed(
                    "Received checkpoint of {} when previously {}".format(
                        new_checkpoint, old_checkpoint
                    ), server
                )
            self.checkpoint = new_checkpoint

        return out

    def authenticate(self, token):
        return self._try_fetch(
            '/token/validate',
            method='POST',
            body=urllib.urlencode({
                "token": token,
            })
        )
