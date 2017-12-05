import json

from mock import Mock, patch

from fixtures import service_account_response
from groupy.client import Groupy, HTTPClient
from groupy.resources import MappedPermission


def test_service_account(service_account_response):
    res = Mock()
    res.body = json.dumps(service_account_response)
    mock_fetch = Mock()
    mock_fetch.side_effect = [res]
    with patch.object(HTTPClient, 'fetch', mock_fetch):
        client = Groupy(['localhost:8000'])
        service = client.users.get('service@a.co')
        assert service.enabled
        assert service.groups == {}
        assert service.passwords == []
        assert service.permissions == [MappedPermission(
            permission=u'sudo',
            argument=u'shell',
            granted_on=1452796706.894347,
            distance=None,
            path=None,
        )]
        expected = service_account_response['data']['user']['service_account']
        assert service.service_account == expected
