import duckdb

from ..models.query import QueryResult
from ..errors import UnsafeQueryError, QueryExecutionError
from ..config import config


class QueryService:
    """Service for SQL query execution."""

    def __init__(self, connection: duckdb.DuckDBPyConnection):
        self.con = connection

    def is_safe_query(self, sql: str) -> bool:
        """Check if SQL query is safe (read-only)."""
        sql_upper = sql.upper()
        return not any(keyword in sql_upper for keyword in config.forbidden_keywords)

    def execute_query(self, sql: str) -> QueryResult:
        """Execute a SQL query and return results."""
        if not self.is_safe_query(sql):
            return QueryResult(error="Unsafe SQL detected. Destructive statements are not allowed.")

        try:
            df = self.con.execute(sql).fetchdf()
            return QueryResult(
                columns=df.columns.tolist(),
                rows=df.astype(str).values.tolist()
            )
        except Exception as e:
            return QueryResult(error=str(e))
