from dataclasses import dataclass
from typing import Optional


@dataclass
class EnvironmentConfiguration:
    name: str
    version: Optional[str]
    build_timeout: Optional[int]
