# Changelog

All notable changes to Data Lens will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Multi-file support (join across files)
- Persistent sessions (save/restore database state)
- Export query results (CSV, Excel, JSON)
- Streaming for large files
- Custom file encoding support
- Query history and caching

---

## [0.1.0] - 2024-11-15

### Added
- Initial release of Data Lens
- MCP server for spreadsheet analysis with natural language queries
- DuckDB integration for fast SQL analytics
- Support for multiple file formats:
  - Excel (.xlsx) with multi-sheet support
  - CSV (.csv) and TSV (.tsv)
  - Parquet (.parquet) with native DuckDB reader
- 8 MCP tools:
  - `load_file`: Load spreadsheets into DuckDB
  - `list_files`: List loaded files
  - `list_tables`: List available tables
  - `list_columns`: Get column information
  - `preview_rows`: Preview table data
  - `get_schema`: Get full schema with sample values
  - `run_sql`: Execute DuckDB SQL queries
  - `clear_all`: Reset database
- Text-to-SQL prompt guide for LLM assistance
- SQL safety checks (read-only queries)
- Automatic table name sanitization
- Schema introspection with sample values
- In-memory database for fast queries
- Comprehensive documentation:
  - README with conversational examples
  - USAGE_GUIDE with 4 detailed workflows
  - TECHNICAL deep-dive documentation
  - TROUBLESHOOTING guide
- GitHub Actions for CI/CD:
  - Automated testing on push/PR
  - PyPI publishing on version tags
  - MCP Registry publishing
- MIT License
- Python 3.11+ support

### Technical Details
- DuckDB for OLAP-optimized analytics
- pandas for Excel/CSV file reading
- FastMCP framework for MCP server
- Type hints and Pydantic validation
- Read-only SQL enforcement (blocks DROP, DELETE, UPDATE, ALTER, CREATE TABLE)

---

## Release Notes

### 0.1.0 - Initial Release

Data Lens launches as an MCP server that brings natural language querying to your spreadsheets.

**Key Features:**
- Ask questions about your data in plain English
- Instant answers powered by DuckDB
- Support for Excel, CSV, and Parquet files
- Read-only safety (never modifies your files)
- Fast in-memory analytics
- Multi-sheet Excel support

**Getting Started:**
```bash
# Install
pip install data-lens

# Or with uvx
uvx data-lens
```

**Example Usage:**
```
You: Load /path/to/sales.xlsx
Claude: Loaded 3 tables: q1_sales, q2_sales, summary

You: What are the top 5 products by revenue?
Claude: [Generates and executes SQL, returns formatted results]
```

See [USAGE_GUIDE.md](USAGE_GUIDE.md) for comprehensive examples and workflows.

---

## Versioning Guide

**MAJOR version** (x.0.0): Incompatible API changes
**MINOR version** (0.x.0): New features (backward compatible)
**PATCH version** (0.0.x): Bug fixes (backward compatible)

---

[Unreleased]: https://github.com/yourusername/data-lens/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/yourusername/data-lens/releases/tag/v0.1.0
