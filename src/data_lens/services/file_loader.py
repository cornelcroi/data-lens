import re
from pathlib import Path
from typing import List

import pandas as pd
import duckdb

from ..errors import UnsupportedFormatError, FileLoadError


class FileLoaderService:
    """Service for loading files into DuckDB."""

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.con = connection

    @staticmethod
    def sanitize_table_name(source: str) -> str:
        """Convert a file or sheet name into a safe SQL table name."""
        name = Path(source).stem
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        return name.lower()

    def load_file(self, file_path: str) -> List[str]:
        """Load a file into DuckDB and return table names."""
        path = Path(file_path)

        if not path.exists():
            raise FileLoadError(f"File not found: {file_path}")

        if not path.is_file():
            raise FileLoadError(f"Not a file: {file_path}")

        ext = path.suffix.lower().lstrip(".")

        if ext == "xlsx":
            return self._load_excel(file_path)
        elif ext in ("csv", "tsv"):
            return self._load_csv(file_path)
        elif ext == "parquet":
            return self._load_parquet(file_path)
        else:
            raise UnsupportedFormatError(f"Unsupported file format: {ext}")

    def _load_excel(self, file_path: str) -> List[str]:
        """Load Excel file with multiple sheets."""
        tables = []
        excel = pd.ExcelFile(file_path)

        for sheet in excel.sheet_names:
            df = excel.parse(sheet)
            table = self.sanitize_table_name(sheet)
            self.con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
            tables.append(table)

        return tables

    def _load_csv(self, file_path: str) -> List[str]:
        """Load CSV or TSV file."""
        df = pd.read_csv(file_path)
        table = self.sanitize_table_name(file_path)
        self.con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
        return [table]

    def _load_parquet(self, file_path: str) -> List[str]:
        """Load Parquet file using DuckDB native reader."""
        table = self.sanitize_table_name(file_path)
        self.con.execute(f"CREATE TABLE {table} AS SELECT * FROM parquet_scan('{file_path}')")
        return [table]
