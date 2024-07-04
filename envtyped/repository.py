from pathlib import Path
from typing import (
    Dict,
    Optional,
    Protocol,
    TypeVar,
)

T = TypeVar("T")


class Repository(Protocol):
    def load_config(self) -> bool: ...

    def __getitem__(self, key: str) -> Optional[str]: ...

    def __contains__(self, key: str) -> bool: ...


class RepositoryEnv(Repository):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.config: Dict[str, str] = {}

    def load_config(self) -> bool:
        if not Path(self.file_path).exists():
            raise FileNotFoundError(f"File {self.file_path} not found")

        with open(self.file_path, "r") as f:
            for line in f:
                if line.startswith("#"):
                    continue

                key, value = line.strip().split("=")
                key = key.strip()
                value = value.strip()
                self.config[key] = value

        return True

    def __getitem__(self, key: str) -> Optional[str]:
        return self.config[key]

    def __contains__(self, key: str) -> bool:
        return key in self.config
