import pytest
from mock import patch

from envtyped import RepositoryEnv


@pytest.fixture
def repository():
    return RepositoryEnv(".env")


def test_load_config_not_found(repository):
    with pytest.raises(FileNotFoundError):
        repository.load_config()


def test_get(repository):
    with patch.object(repository, "config", {"TEST": "test"}):
        assert repository["TEST"] == "test"


def test_get_not_found(repository):
    with pytest.raises(KeyError):
        repository["NOT_EXIST"]


def test_contains(repository):
    with patch.object(repository, "config", {"TEST": "test"}):
        assert "TEST" in repository
        assert "NOT_EXIST" not in repository
