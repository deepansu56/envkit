"""配置装载。"""

from __future__ import annotations

from envkit import get_bool, load_settings


def test_env_overrides_default():
    settings = load_settings({"PORT": 8080}, env={"PORT": "9090"})
    assert settings["PORT"] == "9090"


def test_falls_back_to_default():
    settings = load_settings({"PORT": 8080, "HOST": "localhost"}, env={})
    assert settings == {"PORT": 8080, "HOST": "localhost"}


def test_prefix():
    settings = load_settings({"PORT": 1}, env={"ENVKIT_PORT": "2"}, prefix="ENVKIT_")
    assert settings["PORT"] == "2"


def test_env_keys_are_upper_cased():
    settings = load_settings({"timeout": 5}, env={"TIMEOUT": "30"})
    assert settings["timeout"] == "30"


def test_unrelated_env_ignored():
    settings = load_settings({"PORT": 1}, env={"OTHER": "x"})
    assert settings == {"PORT": 1}


def test_get_bool_truthy_words():
    for word in ("1", "true", "yes", "on", "y", "TRUE"):
        assert get_bool("FLAG", env={"FLAG": word}) is True


def test_get_bool_falsy_words():
    for word in ("0", "false", "no", "off", "n", "FALSE"):
        assert get_bool("FLAG", env={"FLAG": word}) is False


def test_get_bool_trims_whitespace():
    assert get_bool("FLAG", env={"FLAG": "  yes  "}) is True


def test_get_bool_missing_returns_default():
    assert get_bool("FLAG", default=True, env={}) is True
    assert get_bool("FLAG", default=False, env={}) is False


def test_get_bool_unrecognized_returns_default():
    assert get_bool("FLAG", default=True, env={"FLAG": "maybe"}) is True
