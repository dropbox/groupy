import errno
import json
import logging
import socket
from threading import Lock
from typing import NamedTuple, TYPE_CHECKING

from clowncar.backends import Backends
from tornado.httpclient import HTTPClient, HTTPError, HTTPRequest

from groupy import exc
from groupy.collations import Groups, Permissions, ServiceAccounts, Users

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode  # type: ignore

if TYPE_CHECKING:
    from clowncar.server import Server
    from typing import Any, Dict, List, Optional

Checkpoint = NamedTuple("Checkpoint", [("checkpoint", int), ("checkpoint_time", float)])


def _checkpoint_is_greater(a, b):
    # type: (Checkpoint, Checkpoint) -> bool
    """Ensure elements of checkpoint 'a' are all greater than or equal to those in
    checkpoint 'b'."""
    return a.checkpoint >= b.checkpoint and a.checkpoint_time >= b.checkpoint_time


class Groupy(object):
    def __init__(
        self,
        servers,  # type: List[Server]
        partition_key=None,  # type: Optional[str]
        timeout=3,  # type: int
        allow_time_travel=False,  # type: bool
        checkpoint=0,  # type: int
        checkpoint_time=0,  # type: float
        mark_bad_timeout=60,  # type: int
        max_backend_tries=5,  # type: int
        use_ssl=False,  # type: bool
    ):
        # type: (...) -> None
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
            use_ssl (int): whether to connect to backend servers using https
                rather than http.
                TODO(): use_ssl should default to True. It currently defaults
                to False solely to preserve backwards compatibility.
        """

        self._lock = Lock()
        self.timeout = timeout
        self.backends = Backends(servers, partition_key)

        self.checkpoint = Checkpoint(checkpoint, checkpoint_time)

        self.allow_time_travel = allow_time_travel
        self.mark_bad_timeout = mark_bad_timeout
        self.max_backend_tries = max_backend_tries
        self.use_ssl = use_ssl

        self.users = Users(self, "users")
        self.groups = Groups(self, "groups")
        self.permissions = Permissions(self, "permissions")
        self.service_accounts = ServiceAccounts(self, "service_accounts")

    def _try_fetch(self, path, **kwargs):
        # type: (str, **Any) -> Dict[str, Any]
        last_failed_server = None
        for idx in range(self.max_backend_tries):
            try:
                return self._fetch(path, **kwargs)
            except exc.BackendConnectionError as err:
                logging.warning("Marking server {} as dead.".format(err.server.hostname))
                self.backends.mark_dead(err.server, self.mark_bad_timeout)
                last_failed_server = err.server
        raise exc.BackendConnectionError(
            "Tried {} servers, all failed.".format(self.max_backend_tries), last_failed_server
        )

    def _fetch(self, path, **kwargs):
        # type: (str, **Any) -> Dict[str, Any]
        http_client = HTTPClient()
        server = self.backends.server
        protocol = "https" if self.use_ssl else "http"
        url = HTTPRequest(
            "{}://{}:{}{}".format(protocol, server.hostname, server.port, path),
            connect_timeout=self.timeout,
            request_timeout=self.timeout,
            **kwargs
        )
        try:
            out = json.loads(http_client.fetch(url).body)
        except HTTPError as err:
            message = err.message or ""
            if err.code == 599:
                raise exc.BackendConnectionError(message, server)
            if err.response:
                try:
                    out = json.loads(err.response.body)
                    if "status" not in out:
                        raise exc.BackendIntegrityError(message, server)
                except (ValueError, TypeError):
                    raise exc.BackendIntegrityError(message, server)
            else:
                raise exc.BackendIntegrityError(message, server)
        except socket.error as err:
            if err.errno == errno.ECONNREFUSED:
                raise exc.BackendConnectionError("socket error (Connection Refused)", server)
            raise

        with self._lock:
            new_checkpoint = Checkpoint(out["checkpoint"], out["checkpoint_time"])
            old_checkpoint = self.checkpoint
            if (
                not _checkpoint_is_greater(new_checkpoint, old_checkpoint)
                and not self.allow_time_travel
            ):
                raise exc.TimeTravelNotAllowed(
                    "Received checkpoint of {} when previously {}".format(
                        new_checkpoint, old_checkpoint
                    ),
                    server,
                )
            self.checkpoint = new_checkpoint

        return out

    def authenticate(self, token):
        # type: (str) -> Dict[str, Any]
        return self._try_fetch("/token/validate", method="POST", body=urlencode({"token": token}))
