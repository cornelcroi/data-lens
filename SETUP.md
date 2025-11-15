# Setup Guide

Complete setup and configuration guide for Data Lens.

## Installation

### Quick Install (Recommended)

Install via uvx (no repository clone needed):

```bash
uvx data-lens
```

### Development Install

For local development and testing:

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

## Configuration for MCP Clients

### Claude Desktop

**Config file location:**
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

**Configuration:**
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

**Restart Claude Desktop** after changing configuration.

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

### Cursor / Continue.dev

Add to MCP configuration:

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

## Development Configuration

When developing locally, use absolute paths to the virtual environment:

### Claude Desktop (Local Development)

```json
{
  "mcpServers": {
    "data-lens": {
      "command": "/path/to/data-lens/venv/bin/python",
      "args": ["-m", "data_lens.main"]
    }
  }
}
```

### MCP Inspector

**Option 1: Using installed package**
- Command: `uvx`
- Arguments: `["data-lens"]`

**Option 2: Local development**
- Command: `/path/to/data-lens/venv/bin/python`
- Arguments: `["-m", "data_lens.main"]`
- Working Directory: `/path/to/data-lens`

## Testing

### Using MCP Inspector

1. Configure as shown above
2. Click "Connect"
3. Verify 8 tools are available:
   - load_file
   - list_files
   - list_tables
   - list_columns
   - preview_rows
   - get_schema
   - run_sql
   - clear_all

### Test with Sample Data

**Load a file:**
```json
{
  "file_path": "/path/to/data.csv"
}
```

**Get schema:**
```json
{}
```

**Run SQL:**
```json
{
  "sql": "SELECT * FROM tablename LIMIT 5"
}
```

### Example Workflows

**E-commerce Analysis:**
```
1. Load sample_ecommerce_data.csv
2. Ask: "What's the total revenue by category?"
3. Ask: "Which region has the highest sales?"
```

**Employee Analysis:**
```
1. Load sample_employee_data.csv
2. Ask: "What's the average salary by department?"
3. Ask: "Who are the top performers?"
```

**Stock Analysis:**
```
1. Load sample_stock_prices.csv
2. Ask: "Which stock gained the most?"
3. Ask: "What's the average daily volume?"
```

## Sample Questions to Try

### Basic Queries
- "What columns are in the data?"
- "Show me the first 10 rows"
- "How many rows are in the table?"

### Aggregations
- "What's the total/average/sum of [column]?"
- "Count rows by [category]"
- "Show me min and max values"

### Grouping
- "Break down sales by region"
- "Average price by product category"
- "Count orders by month"

### Filtering
- "Show only orders above $1000"
- "Which products sold in January?"
- "Find customers in Europe"

### Advanced
- "Top 5 products by revenue"
- "Month-over-month growth"
- "Compare performance across categories"

## Troubleshooting

### Installation Issues

**Command not found: uvx**
```bash
pip install uv
```

**Import errors after installation**
```bash
pip install --upgrade data-lens
```

### Connection Issues

**Server not showing in client**
1. Verify JSON syntax in config file
2. Restart the client application completely
3. Check client logs for errors

**Tools not available**
1. Ensure server is connected (check status)
2. Try asking: "What tools do you have access to?"
3. Restart the client

### File Loading Issues

**File not found**
- Use absolute paths (e.g., `/home/user/data.csv`)
- Verify file exists: `ls /path/to/file.csv`

**Unsupported format**
- Only .xlsx, .csv, .tsv, .parquet are supported
- Check file extension

**Corrupted file**
- Try opening in Excel/spreadsheet app first
- Verify file is not password-protected

### Query Issues

**SQL syntax errors**
- The AI should auto-retry with corrections
- Use `get_schema` first to see column names
- Column names are case-sensitive

**Permission denied**
- Only SELECT queries allowed
- DROP, DELETE, UPDATE are blocked for safety
- This is by design

### Development Issues

**Tests failing**
```bash
pip install -e ".[dev]"
pytest tests/ -v
```

**Import errors in development**
```bash
source venv/bin/activate
pip install -e "."
```

## Verification Checklist

After setup:
- [ ] Server appears in client's MCP server list
- [ ] Can ask "What MCP servers are connected?"
- [ ] Can load a CSV file successfully
- [ ] Can view schema with `get_schema`
- [ ] Can run a simple SELECT query
- [ ] SQL safety blocks DROP/DELETE/UPDATE
- [ ] Can analyze data with natural language

## Advanced Configuration

### Custom Data Directory

Set environment variables in config:

```json
{
  "mcpServers": {
    "data-lens": {
      "command": "uvx",
      "args": ["data-lens"],
      "env": {
        "DATA_LENS_HOME": "/custom/path"
      }
    }
  }
}
```

### Auto-approve Tools

For trusted environments, auto-approve safe tools:

```json
{
  "mcpServers": {
    "data-lens": {
      "command": "uvx",
      "args": ["data-lens"],
      "autoApprove": [
        "list_tables",
        "list_columns",
        "preview_rows",
        "get_schema"
      ]
    }
  }
}
```

## Getting Help

- Check [README.md](README.md) for overview
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development
- Open an issue on GitHub for bugs
- See [GitHub Issues](https://github.com/cornelcroi/data-lens/issues) for known problems
