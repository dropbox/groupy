import json

from clowncar.server import Server
from mock import Mock, patch
import pytest

from fixtures import user_response
from groupy.client import Groupy, HTTPClient
from groupy.exc import TimeTravelNotAllowed


def test_checkpoint(user_response):
    res1 = Mock()
    res1.body = json.dumps({
        u'checkpoint': 10,
        u'checkpoint_time': 1000,
        u'data': user_response['data'],
        u'status': u'ok',
        })
    res2 = Mock()
    res2.body = json.dumps({
        u'checkpoint': 11,
        u'checkpoint_time': 1001,
        u'data': user_response['data'],
        u'status': u'ok',
        })

    # sunny day
    mock_fetch = Mock()
    mock_fetch.side_effect = [res1, res2]
    with patch.object(HTTPClient, 'fetch', mock_fetch):
        client = Groupy(['localhost:8000'])
        client.users.get('oliver@a.co')
        client.users.get('oliver@a.co')

    # time travel not allowed
    mock_fetch.side_effect = [res2, res1]
    with patch.object(HTTPClient, 'fetch', mock_fetch), pytest.raises(TimeTravelNotAllowed):
        client = Groupy(['localhost:8000'])
        client.users.get('oliver@a.co')
        client.users.get('oliver@a.co')

    # time travel allowed
    mock_fetch.side_effect = [res2, res1]
    with patch.object(HTTPClient, 'fetch', mock_fetch):
        client = Groupy(['localhost:8000'], allow_time_travel=True)
        client.users.get('oliver@a.co')
        client.users.get('oliver@a.co')
