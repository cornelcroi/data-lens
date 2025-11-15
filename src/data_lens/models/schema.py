from typing import Dict, List
from pydantic import BaseModel, Field


class ColumnInfo(BaseModel):
    """Information about a table column."""
    name: str
    type: str


class TableSchema(BaseModel):
    """Schema information for a single table."""
    columns: Dict[str, str] = Field(description="Column name to type mapping")
    sample_values: Dict[str, List[str]] = Field(description="Sample values per column")


class SchemaResponse(BaseModel):
    """Complete schema response with all tables."""
    tables: List[str] = Field(description="List of table names")
    schemas: Dict[str, TableSchema] = Field(description="Schema per table")
