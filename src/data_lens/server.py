import re
from pathlib import Path
from typing import Any, Dict, List

import duckdb
import pandas as pd
from fastmcp import FastMCP

mcp = FastMCP("data-lens")
con = duckdb.connect(database=":memory:")
ACTIVE_FILES: List[str] = []


def sanitize_table_name(source: str) -> str:
    """Convert a file or sheet name into a safe SQL table name."""
    name = Path(source).stem
    name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    return name.lower()


def reset_database():
    """Reset DuckDB connection and clear active files."""
    global con, ACTIVE_FILES
    con.close()
    con = duckdb.connect(database=":memory:")
    ACTIVE_FILES = []


def is_safe_sql(sql: str) -> bool:
    """Check if SQL query is safe (read-only)."""
    forbidden = ["DROP", "DELETE", "UPDATE", "ALTER", "CREATE TABLE"]
    return not any(word in sql.upper() for word in forbidden)


def load_file_to_duckdb(file_path: str) -> List[str]:
    """Load a spreadsheet file into DuckDB and return table names."""
    global con, ACTIVE_FILES

    con.close()
    con = duckdb.connect(database=":memory:")

    ext = Path(file_path).suffix.lower().lstrip(".")
    tables: List[str] = []

    if ext == "xlsx":
        excel = pd.ExcelFile(file_path)
        for sheet in excel.sheet_names:
            df = excel.parse(sheet)
            table = sanitize_table_name(sheet)
            con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
            tables.append(table)

    elif ext in ("csv", "tsv"):
        df = pd.read_csv(file_path)
        table = sanitize_table_name(file_path)
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM df")
        tables.append(table)

    elif ext == "parquet":
        table = sanitize_table_name(file_path)
        con.execute(f"CREATE TABLE {table} AS SELECT * FROM parquet_scan('{file_path}')")
        tables.append(table)

    else:
        raise ValueError(f"Unsupported file format: {ext}")

    ACTIVE_FILES = [file_path]
    return tables


def get_table_schema(table: str) -> Dict[str, Any]:
    """Extract column information and sample values from a table."""
    rows = con.execute(f"DESCRIBE {table}").fetchall()
    columns = {r[0]: r[1] for r in rows}

    df = con.execute(f"SELECT * FROM {table} LIMIT 5").fetchdf()
    sample_values = {col: df[col].astype(str).tolist() for col in df.columns}

    return {"columns": columns, "sample_values": sample_values}


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
    tables = load_file_to_duckdb(file_path)
    return {"file_path": file_path, "tables": tables, "mode": "single_file"}


@mcp.tool()
def list_files() -> Dict[str, Any]:
    """List all files loaded into data-lens in this session."""
    return {"files": ACTIVE_FILES}


@mcp.tool()
def list_tables() -> Dict[str, Any]:
    """List all DuckDB tables currently available."""
    rows = con.execute("SELECT table_name FROM information_schema.tables").fetchall()
    return {"tables": [r[0] for r in rows]}


@mcp.tool()
def list_columns(table: str) -> Dict[str, Any]:
    """List columns for a specific table with their types."""
    rows = con.execute(f"DESCRIBE {table}").fetchall()
    return {"table": table, "columns": [{"name": r[0], "type": r[1]} for r in rows]}


@mcp.tool()
def preview_rows(table: str, limit: int = 5) -> Dict[str, Any]:
    """Return the first N rows of a table."""
    df = con.execute(f"SELECT * FROM {table} LIMIT {limit}").fetchdf()
    return {
        "table": table,
        "limit": limit,
        "columns": df.columns.tolist(),
        "rows": df.astype(str).values.tolist()
    }


@mcp.tool()
def get_schema() -> Dict[str, Any]:
    """Return schema information for all tables including sample values."""
    rows = con.execute("SELECT table_name FROM information_schema.tables").fetchall()
    tables = [r[0] for r in rows]
    schemas = {t: get_table_schema(t) for t in tables}
    return {"tables": tables, "schemas": schemas}


@mcp.tool()
def run_sql(sql: str) -> Dict[str, Any]:
    """Execute a SQL query against the current DuckDB database."""
    if not is_safe_sql(sql):
        return {"error": "Unsafe SQL detected. Destructive statements are not allowed."}

    try:
        df = con.execute(sql).fetchdf()
        return {
            "columns": df.columns.tolist(),
            "rows": df.astype(str).values.tolist()
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
def clear_all() -> Dict[str, Any]:
    """Reset the DuckDB database and remove all loaded files."""
    reset_database()
    return {"status": "OK", "message": "Database reset and all files cleared."}


if __name__ == "__main__":
    mcp.run()
