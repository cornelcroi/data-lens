# Data Lens - Troubleshooting Guide

Solutions to common issues and error messages.

---

## Table of Contents

- [Installation Issues](#installation-issues)
- [Connection Issues](#connection-issues)
- [File Loading Errors](#file-loading-errors)
- [Query Execution Errors](#query-execution-errors)
- [Performance Problems](#performance-problems)
- [Common Error Messages](#common-error-messages)

---

## Installation Issues

### "Command not found: uvx"

**Problem:** `uvx` is not installed.

**Solution:**
```bash
pip install uv
```

Or use pip directly:
```bash
pip install data-lens
```

### "No module named 'data_lens'"

**Problem:** Package not installed correctly.

**Solution:**
```bash
# Uninstall and reinstall
pip uninstall data-lens
pip install data-lens --force-reinstall
```

### Import errors after installation

**Problem:** Dependency conflicts or incomplete installation.

**Solution:**
```bash
# Update all dependencies
pip install --upgrade data-lens

# Or install in isolated environment
python -m venv venv
source venv/bin/activate
pip install data-lens
```

### "ModuleNotFoundError: No module named 'duckdb'"

**Problem:** DuckDB not installed.

**Solution:**
```bash
pip install duckdb pandas openpyxl pyarrow
```

Should be installed automatically, but sometimes fails.

---

## Connection Issues

### "Server not showing in Claude Desktop"

**Problem:** MCP server not configured correctly.

**Solution:**
1. Check config file location:
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. Verify JSON syntax:
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

3. Restart Claude Desktop completely (quit, not just close window)

4. Check logs:
   ```bash
   # macOS
   tail -f ~/Library/Logs/Claude/mcp*.log
   ```

### "Server crashes on startup"

**Problem:** DuckDB initialization failed or missing dependencies.

**Solution:**
1. Test manually:
   ```bash
   uvx data-lens
   ```

2. Check for errors in output

3. Verify dependencies:
   ```bash
   pip list | grep -E "(duckdb|pandas|fastmcp)"
   ```

### "Tools not available in Claude"

**Problem:** Server connected but tools not registered.

**Solution:**
1. Verify server is listed in Claude Desktop settings

2. Try asking: "What tools do you have access to?"

3. If data-lens tools aren't listed, restart server:
   - Quit Claude Desktop
   - Reopen
   - Try again

---

## File Loading Errors

### "Unsupported file format"

**Problem:** File extension not recognized.

**Supported formats:**
- `.xlsx` (Excel)
- `.csv` (Comma-separated)
- `.tsv` (Tab-separated)
- `.parquet` (Parquet)

**Solution:**
```bash
# Check file extension
ls -la your_file.*

# Rename if needed
mv data.txt data.csv
```

### "FileNotFoundError: No such file or directory"

**Problem:** File path is incorrect or doesn't exist.

**Solution:**
1. Verify file exists:
   ```bash
   ls -la /path/to/file.xlsx
   ```

2. Use absolute paths:
   ```
   ❌ load_file("data.csv")
   ✅ load_file("/Users/username/Documents/data.csv")
   ```

3. Check for typos in filename

### "Excel file loading is slow"

**Problem:** Large Excel file with many sheets.

**Diagnosis:**
```
Small file (<100KB): ~200ms
Medium file (1-10MB): 1-3 seconds
Large file (>20MB): 5-10 seconds (normal)
```

**Solutions:**
1. **Convert to CSV or Parquet for speed:**
   ```bash
   # In Python
   import pandas as pd
   df = pd.read_excel("large_file.xlsx")
   df.to_parquet("large_file.parquet")
   ```
   Parquet loads 5-10x faster!

2. **Load specific sheets only:**
   - Save individual sheets as separate CSV files
   - Load only the sheet you need

3. **Excel-specific issues:**
   - Remove unused formatting
   - Delete empty rows/columns
   - Reduce file size

### "CSV encoding errors"

**Problem:** File contains non-UTF-8 characters.

**Error message:**
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x... in position ...
```

**Solution:**
```bash
# Check file encoding
file -I data.csv

# Convert to UTF-8
iconv -f ISO-8859-1 -t UTF-8 data.csv > data_utf8.csv

# Or in Python
import pandas as pd
df = pd.read_csv("data.csv", encoding="latin1")
df.to_csv("data_utf8.csv", encoding="utf-8", index=False)
```

### "Memory error when loading file"

**Problem:** File too large for available RAM.

**Diagnosis:**
```bash
# Check file size
ls -lh data.csv

# Check available memory
free -h  # Linux
vm_stat  # macOS
```

**Solutions:**

1. **Use Parquet (smaller in memory):**
   ```python
   # Convert CSV to Parquet first
   import pandas as pd
   df = pd.read_csv("large.csv")
   df.to_parquet("large.parquet")
   ```

2. **Close other applications** to free RAM

3. **Sample the data:**
   ```bash
   # Take first 100K rows
   head -100000 large.csv > sample.csv
   ```

4. **Use disk-backed DuckDB** (future feature)

---

## Query Execution Errors

### "Unsafe SQL detected"

**Problem:** Query contains destructive statement.

**Blocked keywords:**
- DROP
- DELETE
- UPDATE
- ALTER
- CREATE TABLE

**Solution:**
Use only SELECT queries:
```sql
❌ DELETE FROM sales WHERE region = 'North'
✅ SELECT * FROM sales WHERE region != 'North'

❌ UPDATE products SET price = price * 1.1
✅ SELECT product, price * 1.1 as new_price FROM products

❌ DROP TABLE old_data
✅ Clear database and reload without that table
```

To reset database: Use the `clear_all` tool.

### "Table does not exist"

**Problem:** Referenced table not loaded or wrong name.

**Solution:**

1. **Check loaded tables:**
   ```
   You: What tables do I have?
   Claude: [Uses list_tables tool]
   ```

2. **Verify table name:**
   Table names are sanitized:
   ```
   File: "Sales Report (Q1).xlsx"
   Sheet: "Q1 Sales"
   Table name: "q1_sales"  (lowercase, no spaces/special chars)
   ```

3. **Reload file if needed:**
   ```
   You: Load /path/to/file.xlsx
   ```

### "Column does not exist"

**Problem:** Column name mismatch or typo.

**Solution:**

1. **Check exact column names:**
   ```
   You: What columns are in the sales table?
   Claude: [Uses list_columns tool]
   ```

2. **Case sensitivity:**
   ```sql
   ❌ SELECT Revenue FROM sales  (column is "revenue")
   ✅ SELECT revenue FROM sales
   ```

3. **Common mismatches:**
   ```
   CSV header: "Customer Name"
   DuckDB column: "Customer Name"  (preserves spaces and case!)

   Use: SELECT "Customer Name" FROM table  (quote if spaces/caps)
   ```

### "Syntax error in SQL"

**Problem:** Invalid DuckDB SQL syntax.

**Common mistakes:**

1. **Date functions:**
   ```sql
   ❌ SELECT MONTH(date_column)
   ✅ SELECT EXTRACT(month FROM date_column)
   ```

2. **String concatenation:**
   ```sql
   ❌ SELECT first + ' ' + last
   ✅ SELECT first || ' ' || last
   ```

3. **Limit/Offset:**
   ```sql
   ❌ SELECT * FROM sales LIMIT 10, 20  (MySQL style)
   ✅ SELECT * FROM sales LIMIT 10 OFFSET 20  (DuckDB style)
   ```

### "Division by zero"

**Problem:** Calculating ratio with zero denominator.

**Solution:**
```sql
❌ SELECT revenue / units_sold
✅ SELECT revenue / NULLIF(units_sold, 0)
✅ SELECT CASE WHEN units_sold = 0 THEN NULL ELSE revenue / units_sold END
```

### "Type mismatch error"

**Problem:** Comparing incompatible types.

**Error:**
```
Cannot compare VARCHAR with INTEGER
```

**Solution:**
```sql
❌ SELECT * FROM sales WHERE year = '2024'  (year is INTEGER)
✅ SELECT * FROM sales WHERE year = 2024

❌ SELECT * FROM sales WHERE amount > '1000'  (amount is DOUBLE)
✅ SELECT * FROM sales WHERE amount > 1000

# Or cast:
✅ SELECT * FROM sales WHERE CAST(year AS VARCHAR) = '2024'
```

---

## Performance Problems

### "Queries are very slow"

**Problem:** Large dataset or inefficient query.

**Diagnosis:**

```
Dataset size:
- <100K rows: Queries should be <100ms
- 100K-1M rows: Queries should be <1s
- >1M rows: Queries can take 1-5s
```

**Solutions:**

1. **Add filters to reduce data:**
   ```sql
   ❌ SELECT * FROM sales  (scans all rows)
   ✅ SELECT * FROM sales WHERE date >= '2024-01-01'  (filters first)
   ```

2. **Limit results:**
   ```sql
   ❌ SELECT * FROM large_table
   ✅ SELECT * FROM large_table LIMIT 100
   ```

3. **Avoid SELECT *:**
   ```sql
   ❌ SELECT * FROM sales  (loads all columns)
   ✅ SELECT product, revenue FROM sales  (loads only 2 columns)
   ```

4. **Use aggregations instead of full scans:**
   ```sql
   ❌ Load all rows, then count in application
   ✅ SELECT COUNT(*) FROM sales  (DuckDB counts, much faster)
   ```

### "File loading takes forever"

**Problem:** Large file or slow file format.

**Benchmarks:**
```
CSV (100MB): ~2-3 seconds (normal)
Excel (100MB): ~5-10 seconds (normal)
Parquet (100MB): ~500ms (fast!) ⚡
```

**Solutions:**

1. **Convert to Parquet:**
   ```python
   import pandas as pd
   df = pd.read_csv("slow.csv")
   df.to_parquet("fast.parquet")
   # 10x faster loading!
   ```

2. **Remove empty rows/columns in Excel:**
   - Open in Excel
   - Delete unused sheets
   - Delete empty rows at the end
   - Save

3. **Split large files:**
   ```bash
   # Split CSV into smaller files
   split -l 100000 large.csv part_
   ```

### "High memory usage"

**Problem:** Large dataset loaded in memory.

**Diagnosis:**
```bash
ps aux | grep data-lens
# Check RSS (Resident Set Size)
```

**Expected memory:**
```
File size × 3-5 = Memory usage

Example:
- 100MB CSV → ~400MB RAM
- 1GB CSV → ~4GB RAM
```

**Solutions:**

1. **Use Parquet** (more memory-efficient):
   ```
   CSV: 1GB file → 4GB RAM
   Parquet: 1GB file → 2GB RAM
   ```

2. **Load only needed columns** (future feature)

3. **Sample the data:**
   ```bash
   head -10000 large.csv > sample.csv
   ```

4. **Close and reload:**
   ```
   You: Clear database
   Claude: [Uses clear_all tool]
   Memory freed!
   ```

---

## Common Error Messages

### "RuntimeError: database connection closed"

**Problem:** DuckDB connection was reset.

**Solution:**
```
You: Clear the database and reload the file
Claude: [Uses clear_all, then load_file]
```

### "pandas.errors.ParserError: Error tokenizing data"

**Problem:** Malformed CSV file.

**Causes:**
- Mixed delimiters (commas and tabs)
- Unquoted fields with special chars
- Inconsistent number of columns

**Solution:**
```python
# In Python, diagnose the issue:
import pandas as pd

# Try different options
df = pd.read_csv("file.csv", delimiter="\t")  # Try tab
df = pd.read_csv("file.csv", quotechar="'")   # Try single quotes
df = pd.read_csv("file.csv", on_bad_lines='skip')  # Skip bad lines
```

### "openpyxl.utils.exceptions.InvalidFileException"

**Problem:** Corrupted or invalid Excel file.

**Solution:**
1. Open file in Excel and re-save
2. Export as CSV instead
3. Try LibreOffice to repair

### "pyarrow.lib.ArrowInvalid: Could not open Parquet input source"

**Problem:** Corrupted or incompatible Parquet file.

**Solution:**
```python
# Validate Parquet file
import pyarrow.parquet as pq
table = pq.read_table("file.parquet")
print(table.schema)

# Re-create from CSV if corrupted
df = pd.read_csv("source.csv")
df.to_parquet("repaired.parquet")
```

### "AttributeError: 'DataFrame' object has no attribute 'fetchall'"

**Problem:** Internal error (mixing pandas and DuckDB APIs).

**Solution:**
File an issue on GitHub with:
- File type (CSV, Excel, Parquet)
- File size
- Query that caused error

---

## Getting More Help

### Enable Debug Logging

```bash
export LOG_LEVEL=DEBUG
uvx data-lens 2>&1 | tee debug.log
```

Save output to `debug.log` for analysis.

### Check Versions

```bash
pip show data-lens
pip show duckdb
pip show pandas
```

Update to latest:
```bash
pip install --upgrade data-lens duckdb pandas
```

### Test DuckDB Manually

```python
import duckdb
con = duckdb.connect(":memory:")

# Test basic query
con.execute("SELECT 42 as answer").fetchall()
# Should return: [(42,)]

# Test CSV loading
con.execute("SELECT * FROM read_csv_auto('test.csv') LIMIT 5").fetchall()
```

### Report Issues

When reporting issues, include:
1. Operating system and version
2. Python version (`python --version`)
3. data-lens version (`pip show data-lens`)
4. File format and size
5. Full error message
6. Steps to reproduce
7. Debug logs (if possible)

Open issue: https://github.com/yourusername/data-lens/issues

---

## FAQ

**Q: Why does the first query take longer?**
A: DuckDB initializes on first query (~100ms overhead). Subsequent queries are faster.

**Q: Can I use data-lens offline?**
A: Yes! Everything runs locally. No internet required.

**Q: How do I backup my data?**
A: data-lens is stateless. Your source files ARE your backup. Just keep your Excel/CSV files safe.

**Q: Can I query multiple files at once?**
A: Not yet (planned feature). Currently, loading a new file resets the database.

**Q: Is there a file size limit?**
A: Limited by available RAM. On 16GB system, practical limit is ~2-4GB files.

**Q: Does data-lens modify my files?**
A: No! All operations are read-only. Your source files are never modified.

---

**Still having issues?** Check the [README](README.md) or [TECHNICAL.md](TECHNICAL.md) for more details.
