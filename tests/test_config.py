from __future__ import annotations

import pytest
from mock import patch

from envtyped import Config

from .mock import MockRepository


@pytest.fixture()
def env_setup(monkeypatch):
    monkeypatch.setenv("FROM_ENV", "env")


@pytest.fixture
def config():
    return Config(
        reposetory=MockRepository(
            {"TEST": "test", "TEST2": "test2", "TEST3": "3", "FROM_ENV": "config"}
        )
    )


def test_get(config):
    assert config.get("TEST") == "test"
    assert config.get("TEST2") == "test2"
    assert config.get("TEST3") == "3"


def test_get_throw(config):
    with pytest.raises(KeyError):
        config.get("NOT_EXIST")


def test_get_default(config):
    assert config.get("NOT_EXIST", default="default") == "default"


def test_get_cast(config):
    assert config.get("TEST3", cast=int) == 3


def test_get_cast_function(config):
    assert config.get("TEST3", cast=lambda x: int(x) + 1) == 4


def test_get_cast_class(config):
    class Test:
        def __init__(self, value: str) -> None:
            self.value = value

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Test):
                return False
            return self.value == other.value

    assert config.get("TEST3", cast=Test) == Test("3")


def test_get_env_has_more_priority(config, env_setup):
    assert config.get("FROM_ENV") == "env"


def test_get_env_has_more_priority_default(config, env_setup):
    assert config.get("FROM_ENV", default="default") == "env"


def test_get_optional(config):
    assert config.get("NOT_EXIST", optional=True) is None


def test_get_optional_default(config):
    assert config.get("NOT_EXIST", default="default", optional=True) == "default"


def test_autoload_env_file_lazy():
    config = Config()

    with patch.object(config.reposetory, "load_config", return_value=True) as mock:
        with patch.object(config.reposetory, "config", {"TEST": "test"}):
            assert config.is_loaded is False

            assert config.get("TEST") == "test"
            assert config.get("TEST") == "test"
            assert config.get("TEST") == "test"

            mock.assert_called_once()
            assert config.is_loaded is True
