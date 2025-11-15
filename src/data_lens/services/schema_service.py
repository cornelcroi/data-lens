from typing import Dict, List

import duckdb

from ..models.schema import TableSchema, SchemaResponse, ColumnInfo
from ..config import config


class SchemaService:
    """Service for schema inspection and metadata."""

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.con = connection

    def list_tables(self) -> List[str]:
        """List all tables in the database."""
        rows = self.con.execute("SELECT table_name FROM information_schema.tables").fetchall()
        return [r[0] for r in rows]

    def list_columns(self, table: str) -> List[ColumnInfo]:
        """List columns for a table."""
        rows = self.con.execute(f"DESCRIBE {table}").fetchall()
        return [ColumnInfo(name=r[0], type=r[1]) for r in rows]

    def get_table_schema(self, table: str) -> TableSchema:
        """Get schema with sample values for a table."""
        rows = self.con.execute(f"DESCRIBE {table}").fetchall()
        columns = {r[0]: r[1] for r in rows}

        df = self.con.execute(f"SELECT * FROM {table} LIMIT {config.max_sample_rows}").fetchdf()
        sample_values = {col: df[col].astype(str).tolist() for col in df.columns}

        return TableSchema(columns=columns, sample_values=sample_values)

    def get_all_schemas(self) -> SchemaResponse:
        """Get schemas for all tables."""
        tables = self.list_tables()
        schemas = {t: self.get_table_schema(t) for t in tables}
        return SchemaResponse(tables=tables, schemas=schemas)

    def preview_rows(self, table: str, limit: int = None) -> Dict:
        """Preview first N rows of a table."""
        if limit is None:
            limit = config.max_preview_rows

        df = self.con.execute(f"SELECT * FROM {table} LIMIT {limit}").fetchdf()
        return {
            "table": table,
            "limit": limit,
            "columns": df.columns.tolist(),
            "rows": df.astype(str).values.tolist()
        }
