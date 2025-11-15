from dataclasses import dataclass
from typing import List


@dataclass
class DataLensConfig:
    """Configuration for Data Lens MCP server."""

    database_type: str = ":memory:"
    max_preview_rows: int = 5
    max_sample_rows: int = 5

    forbidden_keywords: List[str] = None

    def __post_init__(self):
        if self.forbidden_keywords is None:
            self.forbidden_keywords = ["DROP", "DELETE", "UPDATE", "ALTER", "CREATE TABLE"]


config = DataLensConfig()
