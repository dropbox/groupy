import pytest

from groupy.client import HTTPClient


@pytest.fixture
def user_response(request):
    return {
        u'checkpoint': 10,
        u'checkpoint_time': 1000,
        u'data': {
            u'groups': {
                u'all-teams': {
                    u'distance': 3,
                    u'name': u'all-teams',
                    u'path': [u'oliver@a.co', u'security-team', u'team-infra', u'all-teams'],
                    u'role': 0,
                    u'rolename': u'member',
                    },
                u'sad-team': {
                    u'distance': 1,
                    u'name':
                    u'sad-team',
                    u'path': [u'oliver@a.co', u'sad-team'],
                    u'role': 0,
                    u'rolename': u'member',
                    },
                u'security-team': {
                    u'distance': 1,
                    u'name': u'security-team',
                    u'path': [u'oliver@a.co', u'security-team'],
                    u'role': 2,
                    u'rolename': u'owner',
                    },
                u'team-infra': {
                    u'distance': 2,
                    u'name': u'team-infra',
                    u'path': [u'oliver@a.co', u'security-team', u'team-infra'],
                    u'role': 0,
                    u'rolename': u'member',
                    }
                },
            u'permissions': [{
                u'argument': u'shell',
                u'distance': 2,
                u'granted_on': 1452796706.894347,
                u'path': [u'oliver@a.co', u'security-team', u'team-infra'],
                u'permission': u'sudo',
                }],
            u'user': {
                u'enabled': True,
                u'metadata': [],
                u'name': u'oliver@a.co',
                u'public_keys': [],
                u'role_user': False,
                }
            },
        u'status': u'ok',
        }
