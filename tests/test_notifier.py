import time
from unittest.mock import patch, MagicMock
from notifier import WeChatNotifier


def make_notifier():
    return WeChatNotifier(
        app_id="test_id",
        app_secret="test_secret",
        template_id="test_template",
        user_openid="test_openid",
    )


@patch("notifier.requests.get")
def test_get_access_token(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"access_token": "token_abc", "expires_in": 7200}
    mock_get.return_value = mock_resp

    n = make_notifier()
    token = n._get_access_token()

    assert token == "token_abc"
    mock_get.assert_called_once()
    assert "appid=test_id" in mock_get.call_args[0][0]


@patch("notifier.requests.get")
def test_access_token_caching(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"access_token": "token_abc", "expires_in": 7200}
    mock_get.return_value = mock_resp

    n = make_notifier()
    n._get_access_token()
    n._get_access_token()

    assert mock_get.call_count == 1


@patch("notifier.requests.post")
@patch("notifier.requests.get")
def test_send_notification(mock_get, mock_post):
    mock_get_resp = MagicMock()
    mock_get_resp.json.return_value = {"access_token": "token_abc", "expires_in": 7200}
    mock_get.return_value = mock_get_resp

    mock_post_resp = MagicMock()
    mock_post_resp.json.return_value = {"errcode": 0, "errmsg": "ok"}
    mock_post.return_value = mock_post_resp

    n = make_notifier()
    result = n.send("Match accepted!")

    assert result is True
    mock_post.assert_called_once()
    call_json = mock_post.call_args[1]["json"]
    assert call_json["touser"] == "test_openid"
    assert call_json["template_id"] == "test_template"


@patch("notifier.requests.post")
@patch("notifier.requests.get")
def test_send_notification_failure(mock_get, mock_post):
    mock_get_resp = MagicMock()
    mock_get_resp.json.return_value = {"access_token": "token_abc", "expires_in": 7200}
    mock_get.return_value = mock_get_resp

    mock_post.side_effect = Exception("network error")

    n = make_notifier()
    result = n.send("Match accepted!")

    assert result is False
