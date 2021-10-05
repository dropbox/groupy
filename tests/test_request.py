import json
from typing import TYPE_CHECKING

import pytest
from mock import Mock, patch
from tornado.httpclient import HTTPRequest

from groupy.client import Groupy, HTTPClient
from tests.fixtures import service_account_response  # noqa: F401

if TYPE_CHECKING:
    from typing import Any, Dict, Text


def test_request_kwargs(service_account_response):  # noqa: F811
    # type: (Dict[Text, Any]) -> None
    mock_fetch = Mock()
    resp = Mock()
    resp.body = json.dumps(service_account_response)

    def check_request_obj(request):
        # type: (HTTPRequest) -> Mock
        assert request.user_agent == "a string"
        assert request.follow_redirects is False
        return resp

    mock_fetch.side_effect = check_request_obj

    with patch.object(HTTPClient, "fetch", mock_fetch):
        # Confirm basic HTTPRequest construction with kwargs works
        http_req_kwargs = {"user_agent": "a string", "follow_redirects": False}
        client = Groupy(["localhost:8000"], request_kwargs=http_req_kwargs)
        client.users.get("service@a.co")
        assert mock_fetch.call_count == 1

        # Confirm overwriting kwargs in individual _fetch calls works
        with pytest.raises(AssertionError):
            client._fetch("/some/path", user_agent="a different string")
        assert mock_fetch.call_count == 2
