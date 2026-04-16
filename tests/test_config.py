import json
import os
import pytest
from config import load_config


def test_load_config_from_file(tmp_path):
    config_data = {
        "scan_interval": 0.5,
        "match_threshold": 0.8,
        "cooldown_seconds": 30,
        "wechat": {
            "app_id": "test_id",
            "app_secret": "test_secret",
            "template_id": "test_template",
            "user_openid": "test_openid",
        },
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    cfg = load_config(str(config_file))
    assert cfg["scan_interval"] == 0.5
    assert cfg["match_threshold"] == 0.8
    assert cfg["cooldown_seconds"] == 30
    assert cfg["wechat"]["app_id"] == "test_id"


def test_load_config_missing_file():
    with pytest.raises(SystemExit):
        load_config("/nonexistent/config.json")


def test_load_config_missing_wechat_keys(tmp_path):
    config_data = {
        "scan_interval": 0.5,
        "match_threshold": 0.8,
        "cooldown_seconds": 30,
        "wechat": {
            "app_id": "test_id",
            # missing app_secret, template_id, user_openid
        },
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    with pytest.raises(SystemExit):
        load_config(str(config_file))


def test_load_config_defaults(tmp_path):
    config_data = {
        "wechat": {
            "app_id": "id",
            "app_secret": "secret",
            "template_id": "tmpl",
            "user_openid": "openid",
        }
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))

    cfg = load_config(str(config_file))
    assert cfg["scan_interval"] == 0.5
    assert cfg["match_threshold"] == 0.8
    assert cfg["cooldown_seconds"] == 30
