from typing import TYPE_CHECKING

from groupy import exc
from groupy.resources import Group, Permission, ServiceAccount, User

if TYPE_CHECKING:
    from typing import Any, Dict, Iterator, Optional
    from groupy.client import Groupy


class Collection(object):
    def __init__(self, client, name):
        # type: (Groupy, str) -> None
        self.client = client
        self.name = name

    def _get(self, resource=None):
        # type: (Optional[str]) -> Dict[str, Any]
        path = "/{}".format(self.name)
        if resource:
            path += "/{}".format(resource)
        response = self.client._try_fetch(path)
        self._check_error(response)
        return response

    @staticmethod
    def _check_error(response):
        # type: (Dict[str, Any]) -> None
        if response["status"] == "ok":
            return

        combined = []
        for error in response["errors"]:
            code, message = error["code"], error["message"]
            if code == 404:
                raise exc.ResourceNotFound(message)
            combined.append("{}: {}".format(code, message))

        raise exc.ResourceError(", ".join(combined))

    def __iter__(self):
        # type: () -> Iterator[object]
        response = self._get()
        for resource in response["data"][self.name]:
            yield resource


class Groups(Collection):
    def get(self, resource):
        # type: (str) -> Group
        return Group.from_payload(self._get(resource))


class Users(Collection):
    def get(self, resource):
        # type: (str) -> User
        return User.from_payload(self._get(resource))


class ServiceAccounts(Collection):
    def get(self, resource):
        # type: (str) -> User
        """Service accounts do not (yet) have their own meaningful class."""
        return ServiceAccount.from_payload(self._get(resource))


class Permissions(Collection):
    def get(self, resource):
        # type: (str) -> Permission
        return Permission.from_payload(self._get(resource))
