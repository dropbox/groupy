from collections import namedtuple

MappedPermission = namedtuple('MappedPermission',
                              ['permission', 'argument', 'granted_on',
                                  'distance', 'path'])

UserMetadata = namedtuple('UserMetadata',
                          ['key', 'value', 'last_modified'])


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
    def __init__(self, groups, users, subgroups, permissions, audited, contacts):
        self.groups = ResourceDict(groups)
        self.users = ResourceDict(users)
        self.subgroups = ResourceDict(subgroups)
        self.permissions = [
            MappedPermission(**permission) for permission in permissions
        ]
        self.audited = audited
        self.contacts = contacts

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["data"]["groups"],
            payload["data"]["users"],
            payload["data"]["subgroups"],
            payload["data"]["permissions"],

            # New values may not exist in the JSON objects, so we need to be
            # careful.
            payload["data"].get("audited", False),
            # TODO(lfaraone): Figure out why we don't always return 'group'
            payload["data"].get("group", dict()).get("contacts", dict()),
        )


class User(object):
    def __init__(self, groups, public_keys, permissions, metadata, enabled, passwords,
                 service_account):
        self.groups = ResourceDict(groups)
        self.passwords = passwords
        self.public_keys = public_keys
        self.enabled = enabled
        self.service_account = service_account
        if self.service_account:
            self.permissions = [
                MappedPermission(distance=None, path=None, **permission)
                for permission in permissions
            ]
        else:
            self.permissions = [MappedPermission(**permission) for permission in permissions]
        self.metadata = {
            md["data_key"]: UserMetadata(
                key=md["data_key"], value=md["data_value"],
                last_modified=md["last_modified"])
            for md in metadata
        }

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["data"]["groups"],
            payload["data"]["user"]["public_keys"],
            payload["data"]["permissions"],
            payload["data"]["user"]["metadata"],
            payload["data"]["user"]["enabled"],

            # New values may not exist in the JSON objects, so we need to be careful.
            payload["data"]["user"].get("passwords", []),

            # Optional field only present for service accounts.
            #
            # TODO(rra): ServiceAccount objects should lift these up to top-level properties and
            # User objects should not have this, and we should return a ServiceAccount when
            # retrieving a User with this set.
            payload["data"]["user"].get("service_account"),
        )


class ServiceAccount(User):
    pass


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
