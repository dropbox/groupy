import json
from typing import TYPE_CHECKING

from mock import Mock, patch

from groupy.client import Groupy, HTTPClient
from tests.fixtures import permission_response  # noqa: F401
from tests.fixtures import service_account_response  # noqa: F401

if TYPE_CHECKING:
    from typing import Any, Dict, Text


def test_service_account(service_account_response):  # noqa: F811
    # type: (Dict[Text, Any]) -> None
    res = Mock()
    res.body = json.dumps(service_account_response)
    mock_fetch = Mock()
    mock_fetch.side_effect = [res]
    with patch.object(HTTPClient, "fetch", mock_fetch):
        client = Groupy(["localhost:8000"])
        service = client.users.get("service@a.co")
        assert service.enabled
        assert service.groups == {}
        assert service.passwords == []

        assert len(service.permissions) == 1
        assert service.permissions[0].permission == "sudo"
        assert service.permissions[0].argument == "shell"
        assert service.permissions[0].granted_on == 1452796706.894347
        assert service.permissions[0].distance is None
        assert service.permissions[0].path is None

        expected = service_account_response["data"]["user"]["service_account"]
        assert service.service_account == expected


def test_permission(permission_response):  # noqa: F811
    # type: (Dict[Text, Any]) -> None
    res = Mock()
    res.body = json.dumps(permission_response)
    mock_fetch = Mock()
    mock_fetch.side_effect = [res]
    with patch.object(HTTPClient, "fetch", mock_fetch):
        client = Groupy(["localhost:8000"])
        permission = client.permissions.get("grouper.audit.security")
        assert permission.groups == {}
        assert isinstance(permission.audited, bool)
        assert permission.audited is False
