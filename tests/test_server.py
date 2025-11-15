import re
from pathlib import Path

import pytest

from data_lens.server import (
    is_safe_sql,
    load_file_to_duckdb,
    sanitize_table_name,
)


def test_sanitize_table_name():
    assert sanitize_table_name("Sales Data 2024.xlsx") == "sales_data_2024"
    assert sanitize_table_name("test-file.csv") == "test_file"
    assert sanitize_table_name("my@file#name.parquet") == "my_file_name"


def test_is_safe_sql():
    assert is_safe_sql("SELECT * FROM sales") is True
    assert is_safe_sql("SELECT COUNT(*) FROM data") is True
    assert is_safe_sql("DROP TABLE users") is False
    assert is_safe_sql("DELETE FROM sales") is False
    assert is_safe_sql("UPDATE users SET name='test'") is False
    assert is_safe_sql("ALTER TABLE sales ADD COLUMN test") is False


def test_load_csv_file(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")

    tables = load_file_to_duckdb(str(csv_file))
    assert len(tables) == 1
    assert tables[0] == "test"


def test_unsupported_file_format(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("some text")

    with pytest.raises(ValueError, match="Unsupported file format"):
        load_file_to_duckdb(str(txt_file))
