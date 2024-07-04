from pathlib import Path

import pytest

from envtyped import Choice, Config, Csv, RepositoryEnv


@pytest.fixture
def config_path():
    return Path(__file__).parent / "files" / ".env"


@pytest.fixture
def config(config_path):
    return Config(reposetory=RepositoryEnv(str(config_path)))


@pytest.mark.parametrize(
    "key, expected_value",
    [
        ("SECRET", "secret"),
        ("HELLO", "world"),
    ],
)
def test_get_existing_string(config, key, expected_value):
    assert config.get(key) == expected_value


@pytest.mark.parametrize(
    "key, expected_value, cast",
    [("NUMBER", "123", None), ("NUMBER", 123, int)],
)
def test_get_existing_number(config, key, expected_value, cast):
    assert config.get(key, cast=cast) == expected_value


def test_get_nonexistent_with_default(config):
    assert config.get("NOT_EXIST", default="default") == "default"


def test_get_commented_key_raises_keyerror(config):
    with pytest.raises(KeyError):
        config.get("# Comment")


def test_get_existing_stripped_string(config):
    assert config.get("STRIPED", cast=str) == "striped"


@pytest.mark.parametrize(
    "key, expected_value, cast",
    [("LETTERS", ["a", "b", "c"], Csv()), ("NUMBERS", [1, 2, 3], Csv(cast=int))],
)
def test_get_existing_csv(config, key, expected_value, cast):
    assert config.get(key, cast=cast) == expected_value


@pytest.mark.parametrize(
    "key, expected_value, cast, default",
    [
        ("LANGUAGE", "en", Choice(["en", "fr"]), None),
        ("CURRENCY", "eur", Choice(["usd", "eur"]), "usd"),
        ("NOT_A_CHOICE", "en", Choice(["en", "fr"]), "en"),
    ],
)
def test_get_choice(config, key, expected_value, cast, default):
    assert config.get(key, cast=cast, default=default) == expected_value


def test_get_invalid_choice_raises_keyerror(config):
    with pytest.raises(KeyError):
        config.get("NOT_A_CHOICE", cast=Choice(["en", "fr"]))


def test_get_invalid_cast_raises_valueerror(config):
    with pytest.raises(ValueError):
        config.get("LANGUAGE", cast=Choice(["gb", "fr"]))
