from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Dict, Text


@pytest.fixture
def service_account_response(request):
    # type: (str) -> Dict[Text, Any]
    return {
        u"checkpoint": 10,
        u"checkpoint_time": 1000,
        u"data": {
            u"groups": {},
            u"permissions": [
                {u"argument": u"shell", u"granted_on": 1452796706.894347, u"permission": u"sudo"}
            ],
            u"user": {
                u"enabled": True,
                u"metadata": [],
                u"name": u"service@a.co",
                u"public_keys": [],
                u"role_user": False,
                u"service_account": {
                    u"description": u"Some service account",
                    u"machine_set": u"shell",
                    u"owner": u"security-team",
                },
            },
        },
        u"status": u"ok",
    }


@pytest.fixture
def permission_response(request):
    # type: (str) -> Dict[Text, Any]
    return {
        u"checkpoint": 3,
        u"checkpoint_time": 1605842894,
        u"data": {
            u"permission": {u"name": "grouper.audit.security"},
            u"groups": {},
            u"service_accounts": {},
            u"audited": False,
        },
        u"status": u"ok",
    }


@pytest.fixture
def user_response(request):
    # type: (str) -> Dict[Text, Any]
    return {
        u"checkpoint": 10,
        u"checkpoint_time": 1000,
        u"data": {
            u"groups": {
                u"all-teams": {
                    u"distance": 3,
                    u"name": u"all-teams",
                    u"path": [u"oliver@a.co", u"security-team", u"team-infra", u"all-teams"],
                    u"role": 0,
                    u"rolename": u"member",
                },
                u"sad-team": {
                    u"distance": 1,
                    u"name": u"sad-team",
                    u"path": [u"oliver@a.co", u"sad-team"],
                    u"role": 0,
                    u"rolename": u"member",
                },
                u"security-team": {
                    u"distance": 1,
                    u"name": u"security-team",
                    u"path": [u"oliver@a.co", u"security-team"],
                    u"role": 2,
                    u"rolename": u"owner",
                },
                u"team-infra": {
                    u"distance": 2,
                    u"name": u"team-infra",
                    u"path": [u"oliver@a.co", u"security-team", u"team-infra"],
                    u"role": 0,
                    u"rolename": u"member",
                },
            },
            u"permissions": [
                {
                    u"argument": u"shell",
                    u"distance": 2,
                    u"granted_on": 1452796706.894347,
                    u"path": [u"oliver@a.co", u"security-team", u"team-infra"],
                    u"permission": u"sudo",
                }
            ],
            u"user": {
                u"enabled": True,
                u"metadata": [],
                u"name": u"oliver@a.co",
                u"public_keys": [],
                u"role_user": False,
            },
        },
        u"status": u"ok",
    }
