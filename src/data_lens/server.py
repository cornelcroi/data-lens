from typing import Any, Dict

from fastmcp import FastMCP

from .database import DuckDBClient
from .services import FileLoaderService, SchemaService, QueryService

mcp = FastMCP("data-lens")
db_client = DuckDBClient()
file_loader = FileLoaderService(db_client.connection)
schema_service = SchemaService(db_client.connection)
query_service = QueryService(db_client.connection)


@mcp.prompt("text_to_sql_guide")
def text_to_sql_guide() -> str:
    """Guide for LLMs on how to use data-lens for Text-to-SQL with DuckDB."""
    return """You are a SQL reasoning assistant for the data-lens MCP server.

Your job is to analyze spreadsheet data by:
1. Inspecting schema using the get_schema tool.
2. Listing tables using list_tables.
3. Listing columns using list_columns.
4. Previewing example rows via preview_rows.
5. Writing correct DuckDB SQL using column names returned from get_schema.
6. Executing SQL using the run_sql tool.
7. Returning clear answers to the user.

Workflow:
1. If the user uploads a file, call load_file.
2. Always call get_schema before writing SQL, unless you already know the schema.
3. Use column names EXACTLY as returned by get_schema, list_columns, or preview_rows.
4. If multiple tables exist, choose the one matching the user's question.
5. If a SQL error occurs, correct the query and retry automatically using run_sql.

Rules:
- Do NOT guess column names.
- Do NOT hallucinate tables.
- Do NOT use DROP, DELETE, UPDATE, ALTER, CREATE TABLE.
- Use DuckDB syntax.
- Use EXTRACT(month FROM date_column) or similar functions for date logic.
- Use CAST(column AS DOUBLE/DATE) if needed.
- Use preview_rows to understand the data content.
- Use list_tables to discover available tables.
- Use list_columns when the user asks about columns.
- Use clear_all to reset the database when needed.

When you answer the user:
- First, ensure your SQL is correct and has been executed via run_sql.
- Display all tabular results (from preview_rows or run_sql) as markdown tables.
- Then summarize the key findings in natural language."""


@mcp.tool()
def load_file(file_path: str) -> Dict[str, Any]:
    """Load a spreadsheet file (Excel/CSV/Parquet) into DuckDB."""
    try:
        db_client.reset()
        file_loader_new = FileLoaderService(db_client.connection)
        global file_loader, schema_service, query_service
        file_loader = file_loader_new
        schema_service = SchemaService(db_client.connection)
        query_service = QueryService(db_client.connection)

        tables = file_loader.load_file(file_path)
        db_client.active_files = [file_path]

        return {"file_path": file_path, "tables": tables, "mode": "single_file"}
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def list_files() -> Dict[str, Any]:
    """List all files loaded into data-lens in this session."""
    return {"files": db_client.active_files}


@mcp.tool()
def list_tables() -> Dict[str, Any]:
    """List all DuckDB tables currently available."""
    tables = schema_service.list_tables()
    return {"tables": tables}


@mcp.tool()
def list_columns(table: str) -> Dict[str, Any]:
    """List columns for a specific table with their types."""
    columns = schema_service.list_columns(table)
    return {"table": table, "columns": [{"name": c.name, "type": c.type} for c in columns]}


@mcp.tool()
def preview_rows(table: str, limit: int = 5) -> Dict[str, Any]:
    """Return the first N rows of a table."""
    return schema_service.preview_rows(table, limit)


@mcp.tool()
def get_schema() -> Dict[str, Any]:
    """Return schema information for all tables including sample values."""
    response = schema_service.get_all_schemas()
    return response.model_dump()


@mcp.tool()
def run_sql(sql: str) -> Dict[str, Any]:
    """Execute a SQL query against the current DuckDB database."""
    result = query_service.execute_query(sql)
    return result.model_dump(exclude_none=True)


@mcp.tool()
def clear_all() -> Dict[str, Any]:
    """Reset the DuckDB database and remove all loaded files."""
    db_client.reset()
    global file_loader, schema_service, query_service
    file_loader = FileLoaderService(db_client.connection)
    schema_service = SchemaService(db_client.connection)
    query_service = QueryService(db_client.connection)

    return {"status": "OK", "message": "Database reset and all files cleared."}


if __name__ == "__main__":
    mcp.run()
