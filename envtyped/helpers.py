from __future__ import annotations

import string
from shlex import shlex
from typing import (
    Callable,
    Generic,
    Optional,
    TypeVar,
    overload,
)

T = TypeVar("T")


class Csv(Generic[T]):
    def __init__(
        self,
        cast: Optional[type | Callable[[str], T]] = None,
        delimiter=",",
        strip=string.whitespace,
    ) -> None:
        self.cast = cast
        self.delimiter = delimiter
        self.strip = strip

    @overload
    def __call__(self: Csv[None], value: Optional[str]) -> list[str]: ...
    @overload
    def __call__(self, value: Optional[str]) -> list[T]: ...

    def __call__(self, value: Optional[str]) -> list[T] | list[str]:
        """The actual transformation"""
        if value is None:
            return []

        splitter = shlex(value, posix=True)
        splitter.escape = ""
        splitter.whitespace = self.delimiter
        splitter.whitespace_split = True

        if self.cast is None:
            return [s.strip(self.strip) for s in splitter]

        return [self.transform(s) for s in splitter]

    def transform(self, s: str) -> T:
        if self.cast is None:
            raise TypeError("Cast is None")

        return self.cast(s.strip(self.strip))


class Choice(Generic[T]):
    def __init__(self, choices: list[T]) -> None:
        self.choices = choices

    @overload
    def __call__(self: Choice[None], value: Optional[str]) -> str: ...
    @overload
    def __call__(self, value: Optional[str]) -> T: ...
    def __call__(self, value: Optional[str]) -> T | str:
        if value not in self.choices:
            raise ValueError(f"Value {value} not in choices {self.choices}")

        return value
