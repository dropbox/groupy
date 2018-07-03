import json

from mock import Mock, patch

from fixtures import service_account_response
from groupy.client import Groupy, HTTPClient


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

        assert len(service.permissions) == 1
        assert service.permissions[0].permission == 'sudo'
        assert service.permissions[0].argument == 'shell'
        assert service.permissions[0].granted_on == 1452796706.894347
        assert service.permissions[0].distance is None
        assert service.permissions[0].path is None

        expected = service_account_response['data']['user']['service_account']
        assert service.service_account == expected
