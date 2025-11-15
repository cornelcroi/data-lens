from typing import List, Optional
from pydantic import BaseModel, Field


class QueryResult(BaseModel):
    """Result of a SQL query execution."""
    columns: Optional[List[str]] = Field(None, description="Column names")
    rows: Optional[List[List[str]]] = Field(None, description="Result rows")
    error: Optional[str] = Field(None, description="Error message if query failed")

    @property
    def success(self) -> bool:
        """Whether the query executed successfully."""
        return self.error is None
