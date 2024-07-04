import os
from typing import (
    Callable,
    Literal,
    Optional,
    TypeVar,
    overload,
)

from envtyped.repository import Repository, RepositoryEnv

T = TypeVar("T")
P = TypeVar("P", bound=type)


class Config:
    is_loaded = False

    def __init__(self, reposetory: Optional[Repository] = None) -> None:
        self.reposetory = reposetory or RepositoryEnv(".env")
        self.is_loaded = False

    @overload
    def get(
        self,
        key: str,
        default: P = ...,
        cast: None = ...,
        optional: Literal[False] = ...,
    ) -> str: ...

    @overload
    def get(
        self,
        key: str,
        default: P = ...,
        cast: None = ...,
        optional: Literal[True] = ...,
    ) -> Optional[str]: ...

    @overload
    def get(
        self,
        key: str,
        default: Optional[T] = ...,
        cast: Optional[Callable[[str], T]] = ...,
        optional: Literal[False] = ...,
    ) -> T: ...

    @overload
    def get(
        self,
        key: str,
        default: Optional[P] = ...,
        cast: Optional[P] = ...,
        optional: Literal[False] = ...,
    ) -> P: ...

    @overload
    def get(
        self,
        key: str,
        default: Optional[T] = ...,
        cast: Optional[Callable[[str], T]] = ...,
        optional: Literal[True] = ...,
    ) -> Optional[T]: ...

    def get(
        self,
        key: str,
        default: Optional[T | str] = None,
        cast: Optional[P | Callable[[str], T]] = None,
        optional: bool = False,
    ) -> Optional[T | P | str]:
        if not self.is_loaded:
            self.is_loaded = self.reposetory.load_config()

        value: Optional[T | str] = None

        if key in os.environ:
            value = os.environ[key]
        elif key in self.reposetory:
            value = self.reposetory[key]
        else:
            if default is not None:
                return default

            if not optional:
                raise KeyError(f"Key {key} not found in config or environment")

            return None

        assert value is not None

        if cast is not None:
            try:
                return cast(value)
            except Exception as e:
                raise ValueError(f"Cannot cast {value} to {cast}") from e

        return value


config = Config()
