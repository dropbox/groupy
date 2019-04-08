import time
from threading import Lock
from typing import TYPE_CHECKING

from clowncar.server import Server

if TYPE_CHECKING:
    from typing import Set


class ServersFileLoader(object):
    def __init__(self, filename, cache_timeout=300):
        # type: (str, int) -> None
        self.filename = filename
        self._lock = Lock()
        self.cache_timeout = cache_timeout
        self._servers = set()  # type: Set[Server]
        self._last_cache = 0.0

    def _load_servers(self):
        # type: () -> None
        servers = set()

        with open(self.filename) as servers_file:
            for line in servers_file:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue

                if line.count(":") != 1:
                    continue

                hostname, port_str = line.split(":")
                try:
                    port = int(port_str)
                except ValueError:
                    continue

                servers.add(Server(hostname, port))

        self._servers = servers

    @property
    def servers(self):
        # type: () -> Set[Server]
        with self._lock:
            now = time.time()
            if self._last_cache + self.cache_timeout > now:
                return self._servers

            self._last_cache = now
            self._load_servers()
            return self._servers

    def __call__(self):
        # type: () -> Set[Server]
        return self.servers
