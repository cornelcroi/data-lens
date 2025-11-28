# Data Lens

**Ask questions about your spreadsheets in plain English. Get instant answers.**

[![PyPI version](https://badge.fury.io/py/data-lens.svg)](https://badge.fury.io/py/data-lens)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is Data Lens?

Stop wrestling with pivot tables and SQL queries. **Data Lens** transforms your spreadsheets into a conversational AI assistant. Just ask questions in plain English and get instant, accurate answers powered by DuckDB.

**With Data Lens:** "What's the average sales by region?" → Get answer instantly

No SQL knowledge required. No formula errors. Just questions and answers.

## See It In Action

*Demo coming soon - spreadsheet analysis in action*

## Why Data Lens?

- **🗣️ Natural Language** - Ask questions like you'd ask a person
- **⚡ Instant Results** - DuckDB-powered analytics, no waiting
- **🔒 100% Local** - Your data never leaves your machine
- **🆓 Completely Free** - No API keys, no subscriptions, no limits
- **📊 Multiple Formats** - Excel, CSV, TSV, Parquet - we handle them all

## Features

- ✅ **Multiple file formats**: Excel (.xlsx), CSV (.csv), TSV (.tsv), Parquet (.parquet)
- ✅ **Multi-sheet Excel support**: Each sheet becomes a separate table
- ✅ **Smart schema detection**: Automatic column type inference
- ✅ **SQL safety**: Blocks destructive operations (DROP, DELETE, UPDATE)
- ✅ **Sample data preview**: See examples before querying
- ✅ **In-memory performance**: Fast DuckDB-powered analytics

## Try It Out

Want to test Data Lens immediately? The repository includes sample datasets you can use:

### Sample Files

Download these files from the repository or create your own:

1. **sample_ecommerce_data.csv** - E-commerce orders with products, regions, payments
2. **sample_employee_data.csv** - Employee records with departments, salaries, performance
3. **sample_stock_prices.csv** - Stock market data with prices and sectors

### Quick Test Queries

Once you've configured Data Lens, try these conversations:

**E-commerce Analysis:**
```
You: Load sample_ecommerce_data.csv

You: What's the total revenue by region?
```
**Result:**
- North America: $2,153.96
- Europe: $578.97
- Asia: $399.85

**Employee Analysis:**
```
You: Load sample_employee_data.csv

You: What's the average salary by department?
```
**Result:**
- Engineering: $76,666.67
- Marketing: $73,500
- Sales: $71,500
- Finance: $70,000
- HR: $68,000

**Stock Market Analysis:**
```
You: Load sample_stock_prices.csv

You: Which company had the highest trading volume?
```
**Result:**
- Tesla (TSLA): 91.5M average volume

These examples demonstrate Data Lens's ability to instantly analyze data without any SQL knowledge!

## Quick Setup

### Claude Desktop

Add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "mcp-data-lens": {
      "command": "uvx",
      "args": ["mcp-data-lens"]
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
    "mcp-data-lens": {
      "command": "uvx",
      "args": ["mcp-data-lens"],
      "autoApprove": ["list_tables", "list_columns", "preview_rows"]
    }
  }
}
```

Reload: Command Palette → "MCP: Reload Servers"

### Other MCP Clients

For Cursor, Continue.dev, or any MCP-compatible client, see [SETUP.md](SETUP.md) for detailed configuration instructions.

## Example Conversations

### Business Analysis

```
You: Load sales_data.xlsx and show me revenue by region

Claude: I've loaded your sales data. Here's the revenue breakdown:
- North America: $2,456,789
- Europe: $1,892,345
- Asia Pacific: $3,124,567

Asia Pacific is your top-performing region with 43% of total revenue.

You: Which products sold best in Europe?

Claude: Top 5 products in Europe by revenue:
1. Premium Widget Pro - $487,234
2. Standard Widget - $312,456
3. Widget Plus - $245,123
4. Mini Widget - $198,765
5. Widget Starter - $156,432
```

### Data Exploration

```
You: I've uploaded customer_data.csv. What insights can you find?

Claude: I've analyzed your customer data (2,847 customers). Here are key insights:

- Average customer lifetime value: $3,245
- 68% of customers are in the 25-45 age group
- Email marketing has 3.2x higher conversion than other channels
- Top 10% of customers generate 41% of total revenue

Would you like me to dig deeper into any of these?

You: Show me monthly growth trends

Claude: Monthly customer acquisition:
- January: 234 new customers (+12% vs Dec)
- February: 267 new customers (+14% vs Jan)
- March: 312 new customers (+17% vs Feb)

You're seeing accelerating growth - Q1 ended 33% higher than it started.
```

### Quick Questions

```
You: Load inventory.csv. How many items are below reorder level?

Claude: 47 items are currently below their reorder levels.
Here are the most critical (< 25% of reorder level):
- SKU-2847: 12 units (need 100)
- SKU-1923: 8 units (need 75)
- SKU-3456: 15 units (need 90)

You: Export a list of all items to reorder

Claude: Here's the full list of 47 items needing reorder:
[Table with SKU, Current Stock, Reorder Level, Qty Needed]
```

> **More examples:** See [USAGE_GUIDE.md](USAGE_GUIDE.md) for detailed workflows and query patterns.

<!-- mcp-name: io.github.cornelcroi/data-lens -->

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

## Supported File Formats

- **Excel (.xlsx)**: Multi-sheet support, each sheet becomes a table
- **CSV (.csv)**: Single table, auto-detects delimiters
- **TSV (.tsv)**: Tab-separated values
- **Parquet (.parquet)**: Columnar format, native DuckDB support

## Limitations

- **Single-file mode**: Loading a new file replaces the previous dataset
- **Read-only**: Only SELECT queries allowed, no data modification
- **No JOINs across files**: Only one file active at a time

## MCP Registry

Data Lens is published to the official [Model Context Protocol Registry](https://registry.modelcontextprotocol.io/) as `io.github.cornelcroi/data-lens`.

Install with:
```bash
uvx data-lens
```


> **Technical deep-dive:** See [TECHNICAL.md](TECHNICAL.md) for architecture details, DuckDB internals, and performance characteristics.

## FAQ

**How is this different from Excel formulas?**
Excel requires you to write formulas and know cell references. Data Lens lets you ask questions in plain English. Instead of `=AVERAGEIF(B:B,"North",C:C)`, just ask "What's the average for North region?"

**What about other SQL clients?**
Traditional SQL clients require you to know SQL syntax. Data Lens translates your questions into SQL automatically. You get the power of SQL without learning it.

**Is my data secure?**
100% secure. Everything runs locally on your machine. Data Lens never sends your data anywhere. No cloud, no API calls, completely private.

**What file size can it handle?**
Data Lens uses in-memory analytics, so it's limited by your RAM. Most spreadsheets under 100MB work great. For larger datasets, consider using database connections (roadmap feature).

**Can I use this in production?**
Yes! Data Lens is production-ready. It's read-only by design (no DROP/DELETE/UPDATE), so it's safe for production data. Use it for reporting, analysis, and insights.

**Why DuckDB?**
DuckDB is like SQLite for analytics - fast, embedded, and needs no setup. It handles complex queries on millions of rows instantly. Perfect for spreadsheet analysis.

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

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

