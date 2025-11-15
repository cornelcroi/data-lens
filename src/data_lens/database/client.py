from typing import List

import duckdb

from ..config import config


class DuckDBClient:
    """DuckDB database client wrapper."""

    def __init__(self):
        self.connection = duckdb.connect(database=config.database_type)
        self.active_files: List[str] = []

    def reset(self):
        """Reset database connection and clear active files."""
        self.connection.close()
        self.connection = duckdb.connect(database=config.database_type)
        self.active_files = []

    def close(self):
        """Close database connection."""
        self.connection.close()
