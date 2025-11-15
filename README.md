# Data Lens

**Analyze spreadsheets with natural language - powered by DuckDB.**

[![PyPI version](https://badge.fury.io/py/data-lens.svg)](https://badge.fury.io/py/data-lens)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

**data-lens** enables AI assistants like Claude to:
- Load spreadsheet files (Excel, CSV, Parquet) into an in-memory database
- Inspect data schemas and preview samples
- Generate and execute SQL queries based on natural language questions
- Provide data analysis results in conversational form

## Features

- ✅ **Multiple file formats**: Excel (.xlsx), CSV (.csv), TSV (.tsv), Parquet (.parquet)
- ✅ **Multi-sheet Excel support**: Each sheet becomes a separate table
- ✅ **Smart schema detection**: Automatic column type inference
- ✅ **SQL safety**: Blocks destructive operations (DROP, DELETE, UPDATE)
- ✅ **Sample data preview**: See examples before querying
- ✅ **In-memory performance**: Fast DuckDB-powered analytics

## Quick Setup

### Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "data-lens": {
      "command": "uvx",
      "args": ["data-lens"]
    }
  }
}
```

Reload: Settings → Developer → Reload MCP Servers

### Kiro IDE

Add to `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "data-lens": {
      "command": "uvx",
      "args": ["data-lens"],
      "autoApprove": ["list_tables", "list_columns", "preview_rows"]
    }
  }
}
```

Reload: Command Palette → "MCP: Reload Servers"

### Other MCP Clients

For Cursor, Continue.dev, or any MCP-compatible client, see [SETUP.md](SETUP.md) for detailed configuration instructions.

## Development Installation

For local development:

```bash
git clone https://github.com/cornelcroi/data-lens
cd data-lens
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

Run tests:
```bash
pytest tests/ -v
```

Run in development mode:
```bash
python -m data_lens.main
```

> **Detailed setup instructions:** See [SETUP.md](SETUP.md) for MCP Inspector, sample datasets, and advanced configuration.

## Available Tools

The server exposes 8 tools for data analysis:

| Tool | Description |
|------|-------------|
| `load_file` | Load a spreadsheet file into DuckDB |
| `list_files` | Show currently loaded files |
| `list_tables` | List all available tables |
| `list_columns` | Show columns for a specific table |
| `preview_rows` | Display first N rows of a table |
| `get_schema` | Get full schema with types and sample values |
| `run_sql` | Execute a SQL query (read-only) |
| `clear_all` | Reset database and clear all data |

## Example Workflow

1. **User**: "I've uploaded sales.xlsx, what's the average amount?"

2. **AI Assistant**:
   - Calls `load_file("sales.xlsx")` → Creates `sales` table
   - Calls `get_schema()` → Sees columns: `date`, `amount`, `product`
   - Generates SQL: `SELECT AVG(amount) FROM sales`
   - Calls `run_sql(...)` → Gets result
   - Responds: "The average amount is $185.40"

## Supported File Formats

- **Excel (.xlsx)**: Multi-sheet support, each sheet becomes a table
- **CSV (.csv)**: Single table, auto-detects delimiters
- **TSV (.tsv)**: Tab-separated values
- **Parquet (.parquet)**: Columnar format, native DuckDB support

## Limitations

- **Single-file mode**: Loading a new file replaces the previous dataset
- **In-memory only**: Data is not persisted between sessions
- **Read-only**: Only SELECT queries allowed, no data modification
- **No JOINs across files**: Only one file active at a time

## MCP Registry

Data Lens is published to the official [Model Context Protocol Registry](https://registry.modelcontextprotocol.io/) as `io.github.cornelcroi/data-lens`.

Install with:
```bash
uvx data-lens
```

## Project Structure

```
data-lens/
├── src/
│   └── data_lens/
│       ├── __init__.py
│       ├── main.py
│       └── server.py
├── tests/
│   └── test_server.py
├── pyproject.toml
├── server.json
├── LICENSE
└── README.md
```

## Architecture

```
User Question → Claude Desktop → MCP Protocol → data-lens server
                                                      ↓
                                                   DuckDB
                                                      ↓
                                                SQL Results
                                                      ↓
                                              Natural Language Answer
```

## Troubleshooting

### Installation Issues

**Command not found: uvx**
```bash
pip install uv
```

**Import errors**
```bash
pip install --upgrade data-lens
```

### File Loading Issues

- Verify file format is supported (.xlsx, .csv, .tsv, .parquet)
- Check file path is absolute or relative to current directory
- Ensure file is not corrupted or password-protected

### SQL Query Issues

- Only SELECT queries are allowed (no DROP, DELETE, UPDATE)
- Column names are case-sensitive
- Use `get_schema` or `list_columns` to verify column names
- The AI should auto-retry with corrected SQL on errors

## Future Enhancements

- [ ] Multi-file mode (load multiple files simultaneously)
- [ ] Persistent database option
- [ ] Query history and caching
- [ ] Export results to files
- [ ] Support for database connections (PostgreSQL, MySQL)
- [ ] Advanced SQL validation

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

---

**Built with FastMCP** | Powered by DuckDB | Made for Claude Desktop
