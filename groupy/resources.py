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
            MappedPermission.from_payload(permission) for permission in permissions
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
        self.permissions = [
            MappedPermission.from_payload(permission) for permission in permissions
        ]
        self.metadata = {
            md["data_key"]: UserMetadata.from_payload(md) for md in metadata
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


class MappedPermission(object):
    def __init__(self, permission, argument, granted_on, distance, path):
        self.permission = permission
        self.argument = argument
        self.granted_on = granted_on
        self.distance = distance
        self.path = path

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["permission"],
            payload["argument"],
            payload["granted_on"],
            payload.get("distance"),
            payload.get("path"),
        )


class UserMetadata(object):
    def __init__(self, key, value, last_modified):
        self.key = key
        self.value = value
        self.last_modified = last_modified

    @classmethod
    def from_payload(cls, payload):
        return cls(
            payload["data_key"],
            payload["data_value"],
            payload["last_modified"],
        )
