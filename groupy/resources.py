from collections import namedtuple

MappedPermission = namedtuple('MappedPermission',
                              ['permission', 'argument', 'granted_on', 'distance', 'path'])


class ResourceDict(dict):
    def __call__(self, direct=False, roles=None):
        if isinstance(roles, basestring):
            roles = [roles]
        new_dict = {}
        for key, value in self.iteritems():
            if direct and value.get("distance", 0) != 1:
                continue
            if roles and value.get("rolename") not in roles:
                continue
            new_dict[key] = value
        return new_dict


class Group(object):
    def __init__(self, groups, users, subgroups, permissions):
        self.groups = ResourceDict(groups)
        self.users = ResourceDict(users)
        self.subgroups = ResourceDict(subgroups)
        self.permissions = [
            MappedPermission(**permission) for permission in permissions
        ]

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["data"]["groups"],
            payload["data"]["users"],
            payload["data"]["subgroups"],
            payload["data"]["permissions"],
        )


class User(object):
    def __init__(self, groups, public_keys, permissions):
        self.groups = ResourceDict(groups)
        self.public_keys = public_keys
        self.permissions = [
            MappedPermission(**permission) for permission in permissions
        ]

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["data"]["groups"],
            payload["data"]["user"]["public_keys"],
            payload["data"]["permissions"]
        )


class Permission(object):
    def __init__(self, groups):
        self.groups = {
            groupname: Group.from_payload({"data": groups[groupname]})
            for groupname in groups
        }

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["data"]["groups"],
        )
