from __future__ import annotations

import pytest

from envtyped import Choice, Csv


def test_csv():
    csv = Csv()
    assert csv("a,b,c") == ["a", "b", "c"]


def test_csv_cast():
    csv = Csv(cast=int)
    assert csv("0,1,2") == [0, 1, 2]


def test_csv_cast_function():
    csv = Csv(cast=lambda x: int(x) + 1)
    assert csv("0,1,2") == [1, 2, 3]


def test_csv_cast_class():
    class Test:
        def __init__(self, value: str) -> None:
            self.value = value

        def __eq__(self, other: object) -> bool:
            if not isinstance(other, Test):
                return False
            return self.value == other.value

    csv = Csv(cast=Test)

    assert csv("a,b,c") == [Test("a"), Test("b"), Test("c")]


def test_choise():
    chose = Choice(["a", "b", "c"])
    assert chose("a") == "a"
    assert chose("b") == "b"
    assert chose("c") == "c"

    with pytest.raises(ValueError):
        chose("d")
