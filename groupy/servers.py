import time
from threading import Lock

from clowncar.server import Server


class ServersFileLoader(object):
    def __init__(self, filename, cache_timeout=300):
        self.filename = filename
        self._lock = Lock()
        self.cache_timeout = cache_timeout
        self._servers = {}
        self._last_cache = 0

    def _load_servers(self):
        servers = set()

        with open(self.filename) as servers_file:
            for line in servers_file:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue

                if line.count(":") != 1:
                    continue

                hostname, port = line.split(":")
                try:
                    port = int(port)
                except ValueError:
                    continue

                servers.add(Server(hostname, port))

        self._servers = servers

    @property
    def servers(self):
        with self._lock:
            now = time.time()
            if self._last_cache + self.cache_timeout > now:
                return self._servers

            self._last_cache = now
            self._load_servers()
            return self._servers

    def __call__(self):
        return self.servers
