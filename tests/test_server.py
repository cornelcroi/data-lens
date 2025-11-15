import duckdb
import pytest

from data_lens.services.file_loader import FileLoaderService
from data_lens.services.query_service import QueryService
from data_lens.errors import UnsupportedFormatError


def test_sanitize_table_name():
    assert FileLoaderService.sanitize_table_name("Sales Data 2024.xlsx") == "sales_data_2024"
    assert FileLoaderService.sanitize_table_name("test-file.csv") == "test_file"
    assert FileLoaderService.sanitize_table_name("my@file#name.parquet") == "my_file_name"


def test_is_safe_query():
    con = duckdb.connect(":memory:")
    query_service = QueryService(con)

    assert query_service.is_safe_query("SELECT * FROM sales") is True
    assert query_service.is_safe_query("SELECT COUNT(*) FROM data") is True
    assert query_service.is_safe_query("DROP TABLE users") is False
    assert query_service.is_safe_query("DELETE FROM sales") is False
    assert query_service.is_safe_query("UPDATE users SET name='test'") is False
    assert query_service.is_safe_query("ALTER TABLE sales ADD COLUMN test") is False
    con.close()


def test_load_csv_file(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")

    con = duckdb.connect(":memory:")
    loader = FileLoaderService(con)
    tables = loader.load_file(str(csv_file))

    assert len(tables) == 1
    assert tables[0] == "test"
    con.close()


def test_unsupported_file_format(tmp_path):
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("some text")

    con = duckdb.connect(":memory:")
    loader = FileLoaderService(con)

    with pytest.raises(UnsupportedFormatError, match="Unsupported file format"):
        loader.load_file(str(txt_file))

    con.close()
