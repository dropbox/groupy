from . import exc
from .resources import User, Group, Permission


class Collection(object):
    def __init__(self, client, name):
        self.client = client
        self.name = name

    def _get(self, resource=None):
        path = "/{}".format(self.name)
        if resource:
            path += "/{}".format(resource)
        response = self.client._try_get(path)
        self._check_error(response)
        return response

    def _check_error(self, response):
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
        response = self._get()
        for resource in response["data"][self.name]:
            yield resource

    def get(self, resource):
        return self.resource.from_payload(self._get(resource))


class Groups(Collection):
    resource = Group


class Users(Collection):
    resource = User


class Permissions(Collection):
    resource = Permission
