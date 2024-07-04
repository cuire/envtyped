from typing import Dict, Optional

from envtyped import Repository


class MockRepository(Repository):
    def __init__(self, config: Dict[str, str]) -> None:
        self.config = config
        self.is_loaded = True

    def load_config(self) -> bool:
        return True

    def __getitem__(self, key: str) -> Optional[str]:
        return self.config[key]

    def __contains__(self, key: str) -> bool:
        return key in self.config
